#!/usr/bin/env python3
"""Task Aggregator — merges outputs from all pipeline stages."""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from .utils import find_latest_glob, load_jsonl_by_uuid, write_json
from .utils import PipelineStage


class TaskAggregator(PipelineStage):
    """Task data aggregator."""

    def __init__(self, output_dir: str = "results/final") -> None:
        super().__init__(output_dir)

    def incremental_aggregate(
        self,
        tasks_dir: str,
        trajectories_dir: Optional[str] = None,
        verifications_dir: Optional[str] = None,
    ) -> str:
        print("Running incremental aggregation...")
        tasks_file = find_latest_glob(tasks_dir, "tasks_*_total_*.jsonl")
        trajectories_file = find_latest_glob(trajectories_dir, "trajectories_*_total_*.jsonl") if trajectories_dir else None
        verifications_file = find_latest_glob(verifications_dir, "verifications_total_*.jsonl") if verifications_dir else None

        print(f"Current data:")
        print(f"  Tasks: {os.path.basename(tasks_file) if tasks_file else 'None'}")
        print(f"  Trajectories: {os.path.basename(trajectories_file) if trajectories_file else 'None'}")
        print(f"  Verifications: {os.path.basename(verifications_file) if verifications_file else 'None'}")

        return self.aggregate_results(
            tasks_file=tasks_file,
            trajectories_file=trajectories_file,
            verifications_file=verifications_file,
            auto_find=False,
        )

    def aggregate_results(
        self,
        tasks_file: Optional[str] = None,
        trajectories_file: Optional[str] = None,
        verifications_file: Optional[str] = None,
        auto_find: bool = True,
        tasks_dir: str = "results/enhanced_test",
        trajectories_dir: str = "results/trajectories",
        verifications_dir: str = "results/verifications",
    ) -> str:
        if auto_find:
            tasks_file = tasks_file or find_latest_glob(tasks_dir, "tasks_*_total_*.jsonl")
            trajectories_file = trajectories_file or find_latest_glob(trajectories_dir, "trajectories_*_total_*.jsonl")
            verifications_file = verifications_file or find_latest_glob(verifications_dir, "verifications_total_*.jsonl")

        print(f"Aggregating results from:")
        print(f"  Tasks: {tasks_file}")
        print(f"  Trajectories: {trajectories_file}")
        print(f"  Verifications: {verifications_file}")

        tasks_data = load_jsonl_by_uuid(tasks_file) if tasks_file else {}
        trajectories_data = load_jsonl_by_uuid(trajectories_file) if trajectories_file else {}
        verifications_data = load_jsonl_by_uuid(verifications_file) if verifications_file else {}

        all_uuids = set()
        all_uuids.update(tasks_data.keys())
        all_uuids.update(trajectories_data.keys())
        all_uuids.update(verifications_data.keys())

        aggregated_results: List[Dict[str, Any]] = []
        for uuid_key in all_uuids:
            task = tasks_data.get(uuid_key, {})
            trajectory = trajectories_data.get(uuid_key, {})
            verification = verifications_data.get(uuid_key, {})

            aggregated_results.append({
                "uuid": uuid_key,
                "domain": task.get("domain", trajectory.get("domain", "unknown")),
                "seed": task.get("seed", ""),
                "question": task.get("question", trajectory.get("question", "")),
                "ground_truth": task.get("ground_truth", trajectory.get("ground_truth", "")),
                "predicted_answer": trajectory.get("predicted_answer", ""),
                "tools": task.get("tools", trajectory.get("tools", [])),
                "task_stats": verification.get("task_stats", {}),
                "verification": verification.get("verification", {}),
                "trajectory": trajectory.get("trajectory", []),
            })

        domain = "unknown"
        if aggregated_results:
            domain = aggregated_results[0].get("domain", "unknown")

        output_file = os.path.join(self.output_dir, f"aggregated_results_{domain}_{self.run_id}.jsonl")
        with open(output_file, "w", encoding="utf-8") as f:
            for record in aggregated_results:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        stats = self._generate_stats(aggregated_results)
        stats_file = os.path.join(self.output_dir, f"aggregation_stats_{domain}_{self.run_id}.json")
        write_json(stats, stats_file)

        print(f"\nAggregation complete!")
        print(f"Stats:")
        print(f"  Total records: {len(aggregated_results)}")
        print(f"  Pipeline progress: {stats['pipeline_progress']}")

        stage_counts = stats["stage_counts"]
        if stage_counts["verifications"] > 0:
            print(f"  Verified: {stage_counts['verifications']}")
            print(f"  Avg accuracy: {stats['avg_accuracy']:.1f}%")
        elif stage_counts["trajectories"] > 0:
            print(f"  Solved: {stage_counts['trajectories']} (awaiting verification)")
        elif stage_counts["tasks"] > 0:
            print(f"  Tasks generated: {stage_counts['tasks']} (awaiting solving)")

        tool_stats = stats.get("tool_stats", {})
        if tool_stats.get("total_tasks_with_tools", 0) > 0:
            print(f"Tool stats:")
            print(f"  Avg tools per task: {tool_stats['avg_tools_per_task']:.1f}")
            print(f"  Unique tools: {tool_stats['unique_tools_count']}")

        print(f"Output: {os.path.basename(output_file)}")
        return output_file

    def _generate_stats(self, aggregated_results: List[Dict]) -> Dict[str, Any]:
        total = len(aggregated_results)
        complete = sum(1 for r in aggregated_results if r.get("question") and r.get("predicted_answer") and r.get("verification"))

        correct_count = 0
        partial_count = 0
        total_verified = 0
        for record in aggregated_results:
            if record.get("verification"):
                total_verified += 1
                c = record["verification"].get("correct", "no")
                if c == "correct":
                    correct_count += 1
                elif c == "partial":
                    partial_count += 1

        domain_distribution: Dict[str, int] = {}
        for r in aggregated_results:
            d = r.get("domain", "unknown")
            domain_distribution[d] = domain_distribution.get(d, 0) + 1

        tool_calls = []
        for r in aggregated_results:
            tc = r.get("task_stats", {}).get("total_tool_calls", 0) or r.get("tool_calls_count", 0)
            if tc > 0:
                tool_calls.append(tc)
        trajectory_lengths = [len(r.get("trajectory", [])) for r in aggregated_results if r.get("trajectory")]

        tools_per_task = [len(r.get("tools", [])) for r in aggregated_results if r.get("tools")]
        all_tools_used = set()
        for r in aggregated_results:
            all_tools_used.update(r.get("tools", []))

        has_tasks = sum(1 for r in aggregated_results if r.get("question"))
        has_traj = sum(1 for r in aggregated_results if r.get("predicted_answer"))
        has_ver = sum(1 for r in aggregated_results if r.get("verification"))

        if has_ver > 0:
            progress = f"Full pipeline complete ({has_ver} verified)"
        elif has_traj > 0:
            progress = f"Solving complete ({has_traj} solved, awaiting verification)"
        elif has_tasks > 0:
            progress = f"Synthesis complete ({has_tasks} tasks, awaiting solving)"
        else:
            progress = "No data"

        return {
            "total_count": total,
            "complete_count": complete,
            "completeness_rate": complete / total * 100 if total else 0,
            "verified_count": total_verified,
            "correct_count": correct_count,
            "partial_count": partial_count,
            "wrong_count": total_verified - correct_count - partial_count,
            "success_rate": complete / total * 100 if total else 0,
            "avg_accuracy": (correct_count + partial_count) / total_verified * 100 if total_verified else 0,
            "strict_accuracy": correct_count / total_verified * 100 if total_verified else 0,
            "domain_distribution": domain_distribution,
            "avg_tool_calls": sum(tool_calls) / len(tool_calls) if tool_calls else 0,
            "avg_trajectory_length": sum(trajectory_lengths) / len(trajectory_lengths) if trajectory_lengths else 0,
            "tool_stats": {
                "avg_tools_per_task": sum(tools_per_task) / len(tools_per_task) if tools_per_task else 0,
                "min_tools_per_task": min(tools_per_task) if tools_per_task else 0,
                "max_tools_per_task": max(tools_per_task) if tools_per_task else 0,
                "unique_tools_count": len(all_tools_used),
                "total_tasks_with_tools": len(tools_per_task),
            },
            "pipeline_progress": progress,
            "stage_counts": {"tasks": has_tasks, "trajectories": has_traj, "verifications": has_ver},
            "aggregated_at": datetime.now().isoformat(),
        }
