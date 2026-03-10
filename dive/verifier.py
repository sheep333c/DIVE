#!/usr/bin/env python3
"""Task Verifier — validates model responses using Claude single-round judgement."""

import json
import os
import re
import time
import uuid as uuid_mod
import random
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .llm import LLMClient
from .utils import append_jsonl, load_jsonl, write_json
from .utils import PipelineStage


class TaskVerifier(PipelineStage):
    """Task verifier."""

    def __init__(
        self,
        claude_model: str = "claude-sonnet-4-20250514",
        output_dir: str = "verifications",
        delay_strategy: str = "progressive",
        llm_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(output_dir)
        # Per-stage LLM config: api_key, base_url, model, provider
        self.llm_config = llm_config or {}
        self.claude_model = self.llm_config.get("model") or claude_model
        self.delay_strategy = delay_strategy
        self._write_lock = threading.Lock()

    def verify_single_response(
        self, task_data: Dict[str, Any], model_response: str, task_uuid: Optional[str] = None
    ) -> Dict[str, Any]:
        question = task_data.get("question", "")
        ground_truth = task_data.get("ground_truth", "")
        task_uuid = task_uuid or task_data.get("uuid", str(uuid_mod.uuid4()))

        if not question or not ground_truth or not model_response:
            return {"error": "Missing required fields: question, ground_truth, or model_response"}

        task_stats = self._calculate_task_stats(task_data)
        print(
            f"Verifying task {task_uuid[:8]}...: {question[:50]}... "
            f"(rounds: {task_stats['total_rounds']}, tools: {task_stats['total_tool_calls']})"
        )

        claude = LLMClient(
            model=self.claude_model,
            save_json=False,
            api_key=self.llm_config.get("api_key"),
            base_url=self.llm_config.get("base_url"),
            provider=self.llm_config.get("provider"),
        )

        try:
            start_time = time.time()
            verify_prompt = self._build_verify_prompt(question, ground_truth, model_response)
            response = claude.chat_with_tools(
                user_query=verify_prompt, tool_names=[], max_rounds=1, temperature=0.0, reset_history=True,
            )
            verify_time = time.time() - start_time
            verification = self._parse_verification_response(response)

            result = {
                "uuid": task_uuid,
                "question": question,
                "ground_truth": ground_truth,
                "model_response": model_response,
                "verification": verification,
                "task_stats": task_stats,
                "verify_time": verify_time,
                "verified_at": datetime.now().isoformat(),
            }
            print(f"Task {task_uuid[:8]}... verified: {verification.get('correct', 'unknown')}")
            return result
        except Exception as e:
            print(f"Task {task_uuid[:8]}... verification failed: {e}")
            return {
                "uuid": task_uuid,
                "question": question,
                "ground_truth": ground_truth,
                "model_response": model_response,
                "task_stats": task_stats,
                "error": str(e),
                "verified_at": datetime.now().isoformat(),
            }

    def _calculate_task_stats(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        trajectory = task_data.get("trajectory", [])
        assistant_rounds = len([m for m in trajectory if m.get("role") == "assistant"])

        total_tool_calls = task_data.get("tool_calls_count", 0)
        if total_tool_calls == 0:
            for msg in trajectory:
                if msg.get("role") == "assistant":
                    total_tool_calls += len(msg.get("tool_calls", []) or [])

        tool_usage: Dict[str, int] = {}
        for msg in trajectory:
            if msg.get("role") == "assistant":
                for call in msg.get("tool_calls", []) or []:
                    fn = call.get("function", {})
                    tn = fn.get("name", "unknown")
                    tool_usage[tn] = tool_usage.get(tn, 0) + 1

        return {
            "total_rounds": assistant_rounds,
            "total_tool_calls": total_tool_calls,
            "unique_tools_used": len(tool_usage),
            "tool_usage_distribution": tool_usage,
            "solve_time_seconds": round(task_data.get("solve_time", 0), 2),
            "avg_tools_per_round": round(total_tool_calls / max(assistant_rounds, 1), 2),
        }

    def _calculate_batch_stats(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not results:
            return {
                "avg_rounds": 0, "avg_tool_calls": 0, "avg_solve_time": 0,
                "total_tool_calls": 0, "unique_tools_count": 0,
                "avg_unique_tools_per_task": 0, "top_tools": [],
            }
        total_rounds = sum(r.get("task_stats", {}).get("total_rounds", 0) for r in results)
        total_tool_calls = sum(r.get("task_stats", {}).get("total_tool_calls", 0) for r in results)
        total_solve_time = sum(r.get("task_stats", {}).get("solve_time_seconds", 0) for r in results)

        all_tool_usage: Dict[str, int] = {}
        for r in results:
            for tool, count in r.get("task_stats", {}).get("tool_usage_distribution", {}).items():
                all_tool_usage[tool] = all_tool_usage.get(tool, 0) + count

        top = sorted(all_tool_usage.items(), key=lambda x: x[1], reverse=True)
        n = len(results)
        return {
            "avg_rounds": round(total_rounds / n, 1),
            "avg_tool_calls": round(total_tool_calls / n, 1),
            "avg_solve_time": round(total_solve_time / n, 1),
            "total_tool_calls": total_tool_calls,
            "unique_tools_count": len(all_tool_usage),
            "avg_unique_tools_per_task": round(
                sum(r.get("task_stats", {}).get("unique_tools_used", 0) for r in results) / n, 1
            ),
            "top_tools": [f"{t}({c})" for t, c in top[:5]],
        }

    def _calculate_verification_stats_from_file(self, verification_file: str, trajectory_file: str) -> Dict[str, Any]:
        results = [r for r in load_jsonl(verification_file) if "error" not in r]
        total = len(results)
        labels = [r.get("verification", {}).get("correct", "").lower() for r in results]
        correct = sum(1 for l in labels if l in ("correct", "yes"))
        partial = sum(1 for l in labels if l == "partial")
        incorrect = total - correct - partial
        accuracy = correct / max(total, 1) * 100
        task_stats = self._calculate_batch_stats(results)

        return {
            "verification_results": {
                "total_verified": total,
                "correct": correct,
                "partial": partial,
                "incorrect": incorrect,
                "accuracy": round(accuracy, 1),
            },
            "task_solving_stats": task_stats,
            "verification_meta": {
                "trajectory_file": trajectory_file,
                "verification_file": verification_file,
                "verified_at": datetime.now().isoformat(),
                "claude_model": self.claude_model,
                "recalculated_from_file": True,
            },
        }

    def _find_master_verification_file(self, domain: str) -> Optional[str]:
        master = os.path.join(self.output_dir, f"verifications_total_{self.run_id}.jsonl")
        return master if os.path.exists(master) else None

    def _build_verify_prompt(self, question: str, ground_truth: str, model_response: str) -> str:
        return f"""Evaluate the correctness of the model's answer.

QUERY: {question}
REFERENCE ANSWER: {ground_truth}
MODEL ANSWER: {model_response}

Evaluation criteria:
- Compare factual content, not surface format
- Ignore differences in phrasing or presentation
- Focus on whether the core factual claims are correct

Output format:
JUDGEMENT: [correct/partial/incorrect]
EXPLANATION: [Brief justification]

Use "correct" if all key facts match, "partial" if the core answer is right but some details are wrong or missing, "incorrect" if the main answer is wrong."""

    def _parse_verification_response(self, response: str) -> Dict[str, Any]:
        correct_match = re.search(r"JUDGEMENT:\s*(\w+)", response, re.IGNORECASE)
        if not correct_match:
            correct_match = re.search(r"CORRECT:\s*(\w+)", response, re.IGNORECASE)
        explanation_match = re.search(r"EXPLANATION:\s*(.+?)(?=\n|JUDGEMENT:|CORRECT:|$)", response, re.DOTALL)
        raw_label = correct_match.group(1).lower() if correct_match else "unknown"
        # Normalize: "yes" -> "correct" for backward compatibility
        if raw_label == "yes":
            raw_label = "correct"
        elif raw_label == "no":
            raw_label = "incorrect"
        return {
            "correct": raw_label,
            "explanation": explanation_match.group(1).strip() if explanation_match else "No explanation provided",
            "raw_response": response,
        }

    def verify_trajectory_file(self, trajectory_file: str, max_workers: int = 4, domain: str = "medical") -> str:
        tasks = [t for t in load_jsonl(trajectory_file) if "error" not in t]
        if not tasks:
            print("No valid tasks found in trajectory file")
            return ""

        output_file = os.path.join(self.output_dir, "current_batch.jsonl")
        summary_file = os.path.join(self.output_dir, f"verifications_{domain}_summary_{self.run_id}.json")

        print(f"Verifying {len(tasks)} task responses using {max_workers} threads...")

        results: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            def submit_with_delay(task_data, model_response, task_uuid, delay_seconds):
                if delay_seconds > 0:
                    time.sleep(delay_seconds)
                return self.verify_single_response(task_data, model_response, task_uuid)

            futures = []
            for i, task in enumerate(tasks):
                model_response = task.get("predicted_answer", "")
                task_uuid = task.get("uuid", str(uuid_mod.uuid4()))

                delay = 0
                if self.delay_strategy == "progressive":
                    delay = 1 * i + random.uniform(0, 0.5)
                elif self.delay_strategy == "random":
                    delay = random.uniform(0.1, 0.5)

                futures.append(executor.submit(submit_with_delay, task, model_response, task_uuid, delay))

            correct_count = 0
            partial_count = 0
            wrong_count = 0
            with tqdm(total=len(tasks), desc="Verifying responses") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result and "error" not in result:
                        results.append(result)
                        correctness = result.get("verification", {}).get("correct", "unknown")
                        if correctness in ("correct", "yes"):
                            correct_count += 1
                        elif correctness == "partial":
                            partial_count += 1
                        else:
                            wrong_count += 1
                        with self._write_lock:
                            with open(output_file, "a", encoding="utf-8") as f:
                                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                    pbar.update(1)
                    pbar.set_postfix({
                        "C": correct_count,
                        "P": partial_count,
                        "W": wrong_count,
                        "acc": f"{correct_count / max(pbar.n, 1) * 100:.1f}%",
                    })

        master = self._find_master_verification_file(domain)
        if master:
            summary_stats = self._calculate_verification_stats_from_file(master, trajectory_file)
        else:
            summary_stats = self._calculate_verification_stats_from_file(output_file, trajectory_file)

        write_json(summary_stats, summary_file)

        vr = summary_stats.get("verification_results", {})
        ts = summary_stats.get("task_solving_stats", {})
        print(f"\nVerification completed!")
        print(f"Total verified: {vr.get('total_verified', 0)}")
        print(f"Correct: {vr.get('correct', 0)}")
        print(f"Partial: {vr.get('partial', 0)}")
        print(f"Incorrect: {vr.get('incorrect', 0)}")
        print(f"Accuracy (correct only): {vr.get('accuracy', 0):.1f}%")
        print(f"Avg rounds: {ts.get('avg_rounds', 0):.1f}, Avg tool calls: {ts.get('avg_tool_calls', 0):.1f}")

        return output_file
