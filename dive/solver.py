#!/usr/bin/env python3
"""Task Solver — solves tasks using Claude with interleaved thinking and records trajectories."""

import json
import os
import time
import uuid as uuid_mod
import glob
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .llm import LLMClient
from .tool_runner import ToolRunner
from .utils import append_jsonl, count_lines_in_file, find_latest_glob, load_jsonl, write_json
from .utils import PipelineStage


class TaskSolver(PipelineStage):
    """Claude task solver."""

    def __init__(
        self,
        output_dir: str = "trajectories",
        tool_runner: Optional[ToolRunner] = None,
        model: str = "claude-sonnet-4-20250514",
        llm_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(output_dir)
        # Per-stage LLM config: api_key, base_url, model, provider
        self.llm_config = llm_config or {}
        self.model = self.llm_config.get("model") or model
        self.tool_runner = tool_runner or ToolRunner()
        self.registry = self.tool_runner.registry
        self.tool_mapping = self.tool_runner.load_domain_tool_mapping()
        self._write_lock = threading.Lock()

        print(f"Loaded {sum(len(t) for t in self.tool_mapping.values())} tools")

    def _parse_domain(self, domain: str) -> Tuple[str, bool]:
        if domain.endswith("_general"):
            return domain[:-8], True
        return domain, False

    def get_domain_tools(self, domain: str) -> List[str]:
        return self.tool_runner.get_domain_tool_ids(domain)

    def solve_single_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        task_uuid = task_data.get("uuid", str(uuid_mod.uuid4()))
        question = task_data.get("question", "")
        domain = task_data.get("domain", "unknown")

        if not question:
            return {"error": "No question provided"}

        task_tools = task_data.get("tools", [])
        if not task_tools:
            print(f"Warning: Task {task_uuid[:8]} has no tools field, using all domain tools")
            task_tools = self.get_domain_tools(domain)

        tools, tool_stats = self.tool_runner.verify_tools(task_tools, domain)
        print(f"Solving task {task_uuid[:8]}...: {question[:50]}... (using {len(tools)} tools: {tool_stats})")

        claude = LLMClient(
            model=self.model,
            save_json=False,
            tool_runner=self.tool_runner,
            api_key=self.llm_config.get("api_key"),
            base_url=self.llm_config.get("base_url"),
            provider=self.llm_config.get("provider"),
        )

        try:
            start_time = time.time()
            response = claude.chat_with_tools(
                user_query=question,
                tool_names=tools,
                max_rounds=30,
                temperature=0.3,
                reset_history=True,
            )
            solve_time = time.time() - start_time
            trajectory = claude.conversation_history

            tool_calls_count = sum(
                len(msg.get("tool_calls", []) or [])
                for msg in trajectory if msg.get("role") == "assistant"
            )

            result = {
                "uuid": task_uuid,
                "question": question + " Please provide the final answer in the format of 'The final answer is: <answer>.'",
                "predicted_answer": response,
                "ground_truth": task_data.get("ground_truth", ""),
                "domain": domain,
                "tools": tools,
                "solve_time": solve_time,
                "trajectory": trajectory,
                "tool_calls_count": tool_calls_count,
                "solved_at": datetime.now().isoformat(),
            }
            print(f"Task {task_uuid[:8]}... completed in {solve_time:.2f}s with {tool_calls_count} tool calls")
            return result
        except Exception as e:
            print(f"Task {task_uuid[:8]}... failed: {e}")
            return {
                "uuid": task_uuid,
                "question": question,
                "domain": domain,
                "tools": tools,
                "error": str(e),
                "solved_at": datetime.now().isoformat(),
            }

    def _save_trajectory_stats(self, trajectory_file: str, stats_file: str, total_input_tasks: int) -> None:
        if not trajectory_file or not os.path.exists(trajectory_file):
            return

        stats: Dict[str, Any] = {
            "total_input_tasks": total_input_tasks,
            "successfully_solved": 0,
            "failed_tasks": 0,
            "tool_calls_stats": {"total_tool_calls": 0, "avg_tool_calls_per_task": 0, "min_tool_calls": float("inf"), "max_tool_calls": 0},
            "trajectory_stats": {"avg_trajectory_length": 0, "min_trajectory_length": float("inf"), "max_trajectory_length": 0},
            "solve_time_stats": {"total_solve_time": 0, "avg_solve_time": 0, "min_solve_time": float("inf"), "max_solve_time": 0},
            "tool_usage_distribution": {},
            "domain_distribution": {},
            "generated_at": datetime.now().isoformat(),
        }

        tool_calls_list: List[int] = []
        trajectory_lengths: List[int] = []
        solve_times: List[float] = []

        for record in load_jsonl(trajectory_file):
            if "error" in record:
                stats["failed_tasks"] += 1
            else:
                stats["successfully_solved"] += 1
                tc = record.get("tool_calls_count", 0)
                tool_calls_list.append(tc)
                stats["tool_calls_stats"]["total_tool_calls"] += tc
                traj = record.get("trajectory", [])
                trajectory_lengths.append(len(traj))
                st = record.get("solve_time", 0)
                solve_times.append(st)
                stats["solve_time_stats"]["total_solve_time"] += st
                d = record.get("domain", "unknown")
                stats["domain_distribution"][d] = stats["domain_distribution"].get(d, 0) + 1
                for msg in traj:
                    if msg.get("role") == "assistant":
                        for call in msg.get("tool_calls", []) or []:
                            fn = call.get("function", {})
                            tn = fn.get("name", "unknown")
                            stats["tool_usage_distribution"][tn] = stats["tool_usage_distribution"].get(tn, 0) + 1

        if tool_calls_list:
            stats["tool_calls_stats"]["avg_tool_calls_per_task"] = sum(tool_calls_list) / len(tool_calls_list)
            stats["tool_calls_stats"]["min_tool_calls"] = min(tool_calls_list)
            stats["tool_calls_stats"]["max_tool_calls"] = max(tool_calls_list)
        else:
            stats["tool_calls_stats"]["min_tool_calls"] = 0

        if trajectory_lengths:
            stats["trajectory_stats"]["avg_trajectory_length"] = sum(trajectory_lengths) / len(trajectory_lengths)
            stats["trajectory_stats"]["min_trajectory_length"] = min(trajectory_lengths)
            stats["trajectory_stats"]["max_trajectory_length"] = max(trajectory_lengths)
        else:
            stats["trajectory_stats"]["min_trajectory_length"] = 0

        if solve_times:
            stats["solve_time_stats"]["avg_solve_time"] = sum(solve_times) / len(solve_times)
            stats["solve_time_stats"]["min_solve_time"] = min(solve_times)
            stats["solve_time_stats"]["max_solve_time"] = max(solve_times)
        else:
            stats["solve_time_stats"]["min_solve_time"] = 0

        stats["success_rate"] = stats["successfully_solved"] / max(total_input_tasks, 1) * 100
        sorted_tools = sorted(stats["tool_usage_distribution"].items(), key=lambda x: x[1], reverse=True)
        stats["top_tools"] = [f"{t}({c})" for t, c in sorted_tools[:10]]

        write_json(stats, stats_file)

    def _find_master_trajectory_file(self, domain: str) -> Optional[str]:
        master = os.path.join(self.output_dir, f"trajectories_{domain}_total_{self.run_id}.jsonl")
        return master if os.path.exists(master) else None

    def solve_task_file(self, task_file: str, domain: str, max_workers: int = 4) -> str:
        tasks = load_jsonl(task_file)
        if not tasks:
            print("No tasks found in file")
            return ""

        output_file = os.path.join(self.output_dir, "current_batch.jsonl")
        stats_file = os.path.join(self.output_dir, f"trajectories_{domain}_summary_{self.run_id}.json")

        print(f"Solving {len(tasks)} tasks using {max_workers} threads...")
        print(f"Output file: {output_file}")

        results: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.solve_single_task, task) for task in tasks]
            with tqdm(total=len(tasks), desc=f"Solving {domain} tasks") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result and "error" not in result:
                        results.append(result)
                        with self._write_lock:
                            with open(output_file, "a", encoding="utf-8") as f:
                                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                    pbar.update(1)
                    pbar.set_postfix({"solved": len(results), "rate": f"{len(results)}/{pbar.n}"})

        print(f"\nSolving completed! {len(results)}/{len(tasks)} succeeded ({len(results)/len(tasks)*100:.1f}%)")

        master = self._find_master_trajectory_file(domain)
        if master:
            total = count_lines_in_file(master)
            self._save_trajectory_stats(master, stats_file, total)
        else:
            self._save_trajectory_stats(output_file, stats_file, len(tasks))

        return output_file
