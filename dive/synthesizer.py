#!/usr/bin/env python3
"""Task Synthesizer — synthesises tasks via iterative evidence collection and task derivation."""

import json
import os
import random
import re
import time
import threading
import uuid as uuid_mod
import yaml
from datetime import datetime
from typing import Any, Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .llm import LLMClient
from .paths import data_path
from .tool_runner import ToolRunner
from .utils import append_jsonl, retry_on_api_error, write_json
from .utils import PipelineStage


def _get_seed(domain: str) -> str:
    """Get initial seed concept(s) for a domain."""
    seed_file = data_path(f"seeds_{domain}.json")
    if seed_file.exists():
        try:
            with open(seed_file, "r", encoding="utf-8") as f:
                all_seeds = json.load(f)
            if all_seeds:
                if domain in ["financial", "financial_general"]:
                    selected = random.sample(all_seeds, min(3, len(all_seeds)))
                else:
                    selected = random.sample(all_seeds, min(1, len(all_seeds)))
                return ", ".join(selected)
        except Exception as e:
            print(f"Warning: Failed to load seed file: {e}")

    fallback_seeds = {
        "medical": ["diabetes", "hypertension", "cancer", "insulin", "aspirin", "penicillin"],
        "biological": ["protein folding", "gene expression", "evolution"],
        "academic": ["machine learning", "climate change", "AI"],
        "financial": ["market volatility", "cryptocurrency"],
        "legal": ["constitutional law", "IP law"],
    }
    domain_seeds = fallback_seeds.get(domain, [f"{domain} topic"])
    selected_fallback = random.sample(domain_seeds, min(3, len(domain_seeds)))
    return ", ".join(selected_fallback)


def _load_exemplars(exemplar_file: Optional[str] = None) -> List[str]:
    """Load exemplars from JSONL file (one {"question": "..."} per line)."""
    if exemplar_file is None:
        exemplar_file = str(data_path("exemplars.jsonl"))

    exemplars: List[str] = []
    try:
        with open(exemplar_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                q = item.get("question", "")
                if q:
                    exemplars.append(q)
    except FileNotFoundError:
        print(f"Warning: Exemplar file not found: {exemplar_file}")
        exemplars = [
            "What is the molecular formula and mechanism of action of aspirin?"
        ]
    return exemplars


def _build_evidence_collection_prompt(
    topic: str,
    domain: str,
    max_steps: int,
    prior_evidence: Optional[List[str]] = None,
) -> str:
    """Build evidence collection prompt for the current round."""
    prior_evidence = prior_evidence or []
    if prior_evidence:
        evidence_text = "\n".join(f"- {entry}" for entry in prior_evidence)
        return f"""Continue research on "{topic}" in {domain} domain.
Step budget: {max_steps}

Previous findings:
{evidence_text}

Based on previous findings, expand the research to broader or deeper aspects. Use diverse tools to retrieve and process new information. Avoid repeating previous findings."""

    return f"""Research "{topic}" in {domain} domain. Use multiple tools to retrieve and process comprehensive and verifiable information from various sources.
Step budget: {max_steps}

Note: Investigate the topic from multiple angles and explore its connections to related entities or concepts.

Strategy: If direct search has limited results, try related concepts, broader categories, or alternative terms. Consider how the different aspects of the topic relate to each other."""


def _build_task_derivation_prompt(
    exemplars: List[str],
    current_question: str,
    evidence_text: str,
    iteration: int = 1,
    seed: Optional[str] = None,
) -> str:
    """Build task derivation prompt with round-aware template."""
    num_exemplars = random.randint(3, 5)
    if exemplars:
        selected = random.sample(exemplars, min(num_exemplars, len(exemplars)))
        examples_text = "\n\n".join(selected)
    else:
        examples_text = "What is the molecular formula and mechanism of action of aspirin?"

    if iteration == 1:
        return f"""Exemplars:
{examples_text}

Seed: {seed or current_question}
Evidence collected: {evidence_text}

Derive a specific and realistic query using the collected data. Base the answer on actual tool results only.

QUERY: [specific query grounded in evidence]
ANSWER: [concise factual answer from tool results only - no explanations, no reasoning, just the key values/facts]
REASONING: [how the evidence supports this query-answer pair]"""

    return f"""Exemplars:
{examples_text}

Current: {current_question}
Evidence collected: {evidence_text}

Refine the question to be more challenging, specific and realistic using the diverse collected data. Base answer on actual tool results only.

EVOLVED_QUERY: [more complex question using collected data]
EVOLVED_ANSWER: [brief, factual answer from tool results - be concise, specific to the question]
REASONING: [what complexity was added]"""


class TaskSynthesizer(PipelineStage):
    """Claude-driven task synthesiser."""

    def __init__(
        self,
        config_file: Optional[str] = None,
        output_dir: str = "results",
        tool_runner: Optional[ToolRunner] = None,
        llm_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(output_dir)

        self.config = self._load_config(config_file)
        # Per-stage LLM config: api_key, base_url, model, provider
        self.llm_config = llm_config or {}

        self.max_workers = self.config.get("max_workers", 2)
        self.retry_count = self.config.get("retry_count", 3)
        self.retry_delay = self.config.get("retry_delay", 30)
        self.save_frequency = self.config.get("save_frequency", 1)

        self.results_lock = threading.Lock()
        self.stats_lock = threading.Lock()
        self.stats: Dict[str, Any] = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "api_errors": 0,
            "start_time": None,
        }

        # Use injected ToolRunner or create one
        self.tool_runner = tool_runner or ToolRunner()
        self.registry = self.tool_runner.registry
        self.tool_mapping = self.tool_runner.load_domain_tool_mapping()

        print(f"Loaded {sum(len(t) for t in self.tool_mapping.values())} tools")
        print(f"Configuration: max_workers={self.max_workers}, retry_count={self.retry_count}")

        self.exemplars = self._load_exemplars()

    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        default_config: Dict[str, Any] = {
            "max_workers": 4,
            "retry_count": 3,
            "retry_delay": 30,
            "save_frequency": 1,
            "claude_model": "claude-sonnet-4-20250514",
            "temperature": 0.7,
            "max_rounds": 3,
            "num_rounds": 3,
            "max_steps": 5,
            "include_toolset": False,
            "include_general": False,
        }
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                default_config.update(user_config)
                print(f"Loaded configuration file: {config_file}")
            except Exception as e:
                print(f"Config file loading failed: {e}, using default configuration")
        return default_config

    def sample_toolset(
        self, domain: str, min_tools: int = 15, max_tools: int = 50, include_general: bool = False
    ) -> List[str]:
        """Get randomised tool IDs for synthesis."""
        domain_tools = self.tool_mapping.get(f"{domain}_tools", {})

        available_tool_ids: List[str] = []
        for _name, tool_id in domain_tools.items():
            try:
                self.registry.create_tool(tool_id)
                available_tool_ids.append(tool_id)
            except Exception:
                continue

        if len(available_tool_ids) < min_tools:
            print(f"Warning: Only {len(available_tool_ids)} tools available for {domain}")
            return available_tool_ids

        random.seed(int(time.time() * 1000000) % 1000000)
        actual_max = min(max_tools, len(available_tool_ids))
        tool_count = random.randint(min_tools, actual_max)
        random.shuffle(available_tool_ids)
        selected = available_tool_ids[:tool_count]

        if include_general:
            general_tools = self.tool_mapping.get("general_tools", {})
            for _name, tool_id in general_tools.items():
                try:
                    self.registry.create_tool(tool_id)
                    selected.append(tool_id)
                except Exception:
                    continue

        print(f"Selected {len(selected)} tools for {domain} domain")
        return selected

    def get_seed(self, domain: str) -> str:
        return _get_seed(domain)

    def _load_exemplars(self) -> List[str]:
        return _load_exemplars()

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    @retry_on_api_error(max_retries=3, delay=30)
    def _synthesize_single_task(self, domain: str, task_id: int) -> Optional[Dict[str, Any]]:
        thread_id = threading.get_ident()
        try:
            print(f"Thread {thread_id}: Starting task {task_id}")
            delay = random.uniform(1, 5)
            time.sleep(delay)

            include_general = self.config.get("include_general", False)
            toolset = self.sample_toolset(domain, include_general=include_general)
            seed = self.get_seed(domain)
            print(f"Task {task_id}: Using seed '{seed}'")

            result = self._run_synthesis_loop(domain, seed, toolset, task_id)

            if result:
                with self.stats_lock:
                    self.stats["completed_tasks"] += 1
                print(f"Task {task_id} completed: {result.get('question', '')[:50]}...")
                return result
            else:
                with self.stats_lock:
                    self.stats["failed_tasks"] += 1
                print(f"Task {task_id} failed")
                return None
        except Exception as e:
            with self.stats_lock:
                self.stats["failed_tasks"] += 1
                if any(kw in str(e).lower() for kw in ["503", "exceeded", "rate_limit"]):
                    self.stats["api_errors"] += 1
            print(f"Task {task_id} error: {e}")
            return None

    def _run_synthesis_loop(
        self, domain: str, seed: str, toolset: List[str], task_id: int
    ) -> Optional[Dict[str, Any]]:
        num_rounds = self.config.get("num_rounds", 3)
        task_uuid = str(uuid_mod.uuid4())
        print(f"Task {task_id} ({task_uuid[:8]}...): Starting {num_rounds}-round synthesis")

        current_question = f"Information related to {seed}"
        evidence: List[str] = []
        derivation_history: List[Dict[str, Any]] = []

        for iteration in range(1, num_rounds + 1):
            print(f"Task {task_id}: Round {iteration}/{num_rounds}")

            new_evidence = self._collect_evidence(
                current_question.replace("Information related to", "").replace("?", "").strip(),
                domain, toolset, evidence, task_uuid, iteration,
            )

            if iteration == 1:
                if len(new_evidence) == 1 and "No specific information gathered" in new_evidence[0]:
                    print(f"Task {task_id}: First evidence collection failed, skipping")
                    return None

            evidence.extend(new_evidence)

            derived_task = self._derive_task(
                current_question, domain, evidence, task_uuid, iteration, seed,
            )
            current_question = derived_task.get("derived_question", current_question)
            derivation_history.append({
                "iteration": iteration,
                "strategy": derived_task.get("strategy", "unknown"),
                "question": current_question,
                "reasoning": derived_task.get("reasoning", ""),
            })
            print(f"Task {task_id}: Round {iteration} derived: {current_question[:50]}...")

        final_derived = derivation_history[-1] if derivation_history else {}
        include_general = self.config.get("include_general", False)
        final_domain = f"{domain}_general" if include_general else domain

        return {
            "uuid": task_uuid,
            "question": current_question,
            "ground_truth": derived_task.get("derived_answer", "Information needs verification"),
            "reasoning": f"Derived through {num_rounds} rounds from seed '{seed}'",
            "domain": final_domain,
            "seed": seed,
            "tools": toolset,
            "created_at": datetime.now().isoformat(),
            "evidence": evidence,
            "derivation_history": derivation_history,
            "rounds_completed": len(derivation_history),
            "final_strategy": final_derived.get("strategy", "unknown"),
        }

    def _collect_evidence(
        self,
        topic: str,
        domain: str,
        toolset: List[str],
        prior_evidence: Optional[List[str]] = None,
        task_uuid: Optional[str] = None,
        current_round: int = 1,
    ) -> List[str]:
        try:
            max_steps = self.config.get("max_steps", 5)
            prior_evidence = prior_evidence or []

            if not topic or not domain:
                raise ValueError("Missing topic or domain parameter")

            current_tools = toolset
            print(f"Round {current_round}: Using {len(current_tools)} tools")

            tool_descriptions = self.tool_runner.get_tool_descriptions(current_tools)

            task_uuid = task_uuid or str(uuid_mod.uuid4())
            claude = LLMClient(
                model=self.llm_config.get("model") or self.config["claude_model"],
                save_json=False,
                tool_runner=self.tool_runner,
                api_key=self.llm_config.get("api_key"),
                base_url=self.llm_config.get("base_url"),
                provider=self.llm_config.get("provider"),
            )

            evidence_prompt = _build_evidence_collection_prompt(
                topic=topic,
                domain=domain,
                max_steps=max_steps,
                prior_evidence=prior_evidence,
            )

            random.seed(int(time.time() * 1000000) % 1000000)
            random.shuffle(current_tools)

            response = claude.chat_with_tools(
                user_query=evidence_prompt,
                tool_names=current_tools,
                max_rounds=max_steps,
                temperature=0.3,
            )

            findings = self._extract_evidence(claude.conversation_history, tool_descriptions)
            return findings
        except Exception as e:
            print(f"Evidence collection failed: {e}")
            return [f"INFO: Failed to gather information about {topic}"]

    def _extract_evidence(
        self, conversation_history: List[Dict], tool_descriptions: Dict[str, str]
    ) -> List[str]:
        information: List[str] = []
        pending_calls: Dict[str, Dict[str, Any]] = {}

        for msg in conversation_history:
            if msg.get("role") == "assistant":
                for call in msg.get("tool_calls", []) or []:
                    fn = call.get("function", {})
                    raw_args = fn.get("arguments", "{}")
                    try:
                        parsed = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                    except (json.JSONDecodeError, TypeError):
                        parsed = {"raw": raw_args}
                    pending_calls[call.get("id", "")] = {
                        "name": fn.get("name", ""),
                        "input": parsed,
                    }
            elif msg.get("role") == "tool":
                tool_call_id = msg.get("tool_call_id", "")
                result_content = str(msg.get("content", ""))[:2000]
                if tool_call_id in pending_calls:
                    call = pending_calls[tool_call_id]
                    tool_name = call["name"]
                    tool_desc = tool_descriptions.get(tool_name, tool_name)
                    information.append(
                        f"INFO: Used {tool_name} ({tool_desc}) with {call['input']} → {result_content}"
                    )
                    del pending_calls[tool_call_id]
                else:
                    information.append(f"INFO: {result_content}")

        return information if information else ["INFO: No specific information gathered"]

    def _derive_task(
        self,
        current_question: str,
        domain: str,
        evidence: List[str],
        task_uuid: Optional[str] = None,
        iteration: int = 1,
        seed: Optional[str] = None,
    ) -> Dict[str, str]:
        try:
            evidence_text = "\n".join(evidence)
            if not current_question:
                raise ValueError("Missing current_question parameter")

            task_uuid = task_uuid or str(uuid_mod.uuid4())
            claude = LLMClient(
                model=self.llm_config.get("model") or self.config["claude_model"],
                save_json=False,
                tool_runner=self.tool_runner,
                api_key=self.llm_config.get("api_key"),
                base_url=self.llm_config.get("base_url"),
                provider=self.llm_config.get("provider"),
            )

            derivation_prompt = self._build_derivation_prompt(
                current_question, evidence_text, "Auto-select best strategy", iteration, seed,
            )
            response = claude.chat_with_tools(
                user_query=derivation_prompt, tool_names=[], max_rounds=1, temperature=0.4,
            )
            return self._parse_derivation_response(response, "Auto-select best strategy")
        except Exception as e:
            print(f"Task derivation failed: {e}")
            return self._get_fallback_derivation(current_question, "Auto-select")

    def _get_fallback_derivation(self, current_question: str, strategy: str) -> Dict[str, str]:
        return {
            "derived_question": "What are the main characteristics and applications based on the current question?",
            "derived_answer": "Detailed information needs verification",
            "reasoning": "Default derivation due to parsing failure",
            "strategy": strategy,
        }

    def _build_derivation_prompt(
        self, current_question: str, evidence_text: str, derivation_strategy: str,
        iteration: int = 1, seed: Optional[str] = None,
    ) -> str:
        return _build_task_derivation_prompt(
            exemplars=self.exemplars,
            current_question=current_question,
            evidence_text=evidence_text,
            iteration=iteration,
            seed=seed,
        )

    def _parse_derivation_response(self, response: str, strategy: str) -> Dict[str, str]:
        question_match = re.search(
            r"(?:QUERY|EVOLVED_QUERY|EVOLVED_QUESTION):\s*(.*?)(?=(?:ANSWER|EVOLVED_ANSWER):|REASONING:|$)",
            response, re.DOTALL | re.IGNORECASE,
        )
        answer_match = re.search(
            r"(?:ANSWER|EVOLVED_ANSWER):\s*(.*?)(?=REASONING:|(?:QUERY|EVOLVED_QUERY|EVOLVED_QUESTION):|$)",
            response, re.DOTALL | re.IGNORECASE,
        )
        reasoning_match = re.search(
            r"REASONING:\s*(.*?)(?=(?:QUERY|EVOLVED_QUERY|EVOLVED_QUESTION):|(?:ANSWER|EVOLVED_ANSWER):|$)",
            response, re.DOTALL | re.IGNORECASE,
        )

        derived_question = ""
        if question_match:
            derived_question = re.sub(r"\n\s*\n", "\n\n", question_match.group(1).strip())
            derived_question = re.sub(r"\n\s+", "\n", derived_question).strip()

        derived_answer = ""
        if answer_match:
            derived_answer = re.sub(r"\n\s*\n", "\n\n", answer_match.group(1).strip())
            derived_answer = re.sub(r"\n\s+", "\n", derived_answer).strip()

        derived_reasoning = ""
        if reasoning_match:
            derived_reasoning = re.sub(r"\n\s*\n", "\n\n", reasoning_match.group(1).strip())
            derived_reasoning = re.sub(r"\n\s+", "\n", derived_reasoning).strip()

        if not derived_question and not derived_answer:
            lines = response.split("\n")
            current_section = None
            question_lines: List[str] = []
            answer_lines: List[str] = []
            reasoning_lines: List[str] = []

            for line in lines:
                line = line.strip()
                line_upper = line.upper()
                if line_upper.startswith("QUERY:") or line_upper.startswith("EVOLVED_QUERY:") or line_upper.startswith("EVOLVED_QUESTION:"):
                    current_section = "question"
                    for p in ["EVOLVED_QUERY:", "EVOLVED_QUESTION:", "QUERY:"]:
                        if line_upper.startswith(p):
                            prefix = p
                            break
                    content = line[len(prefix):].strip()
                    if content:
                        question_lines.append(content)
                elif line_upper.startswith("ANSWER:") or line_upper.startswith("EVOLVED_ANSWER:"):
                    current_section = "answer"
                    prefix = "ANSWER:" if line_upper.startswith("ANSWER:") else "EVOLVED_ANSWER:"
                    content = line[len(prefix):].strip()
                    if content:
                        answer_lines.append(content)
                elif line_upper.startswith("REASONING:"):
                    current_section = "reasoning"
                    content = line[len("REASONING:"):].strip()
                    if content:
                        reasoning_lines.append(content)
                elif line and current_section:
                    if current_section == "question":
                        question_lines.append(line)
                    elif current_section == "answer":
                        answer_lines.append(line)
                    elif current_section == "reasoning":
                        reasoning_lines.append(line)

            if question_lines:
                derived_question = "\n".join(question_lines)
            if answer_lines:
                derived_answer = "\n".join(answer_lines)
            if reasoning_lines:
                derived_reasoning = "\n".join(reasoning_lines)

        if not derived_question:
            derived_question = "Failed to derive question"
        if not derived_answer:
            derived_answer = "Failed to derive answer"
        if not derived_reasoning:
            derived_reasoning = f"Applied {strategy} strategy"

        return {
            "derived_question": derived_question,
            "derived_answer": derived_answer,
            "reasoning": derived_reasoning,
            "strategy": strategy,
            "derivation_timestamp": datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    def _save_stats(self, stats_file: str, output_file: Optional[str] = None) -> None:
        start_time = self.stats.get("start_time") or time.time()
        stats = self._calculate_stats_from_file(output_file) if output_file else {}
        stats["duration_seconds"] = time.time() - start_time
        stats["start_time"] = start_time
        stats["generated_at"] = datetime.now().isoformat()
        write_json(stats, stats_file)

    def _calculate_stats_from_file(self, output_file: str) -> Dict[str, Any]:
        if not output_file or not os.path.exists(output_file):
            return {"total_tasks": 0, "completed_tasks": 0, "failed_tasks": 0, "success_rate": 0}

        completed = 0
        failed = 0
        domain_count: Dict[str, int] = {}
        seed_count: Dict[str, int] = {}
        round_stats: List[int] = []

        try:
            with open(output_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        task = json.loads(line)
                        if "error" in task:
                            failed += 1
                        else:
                            completed += 1
                            d = task.get("domain", "unknown")
                            domain_count[d] = domain_count.get(d, 0) + 1
                            s = task.get("seed", "unknown")[:50]
                            seed_count[s] = seed_count.get(s, 0) + 1
                            round_stats.append(task.get("rounds_completed", 0))
                    except json.JSONDecodeError:
                        failed += 1
        except Exception:
            return {"total_tasks": 0, "completed_tasks": 0, "failed_tasks": 0, "success_rate": 0}

        total = completed + failed
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "failed_tasks": failed,
            "success_rate": completed / max(total, 1) * 100,
            "domain_distribution": domain_count,
            "seed_distribution": dict(list(seed_count.items())[:10]),
            "avg_rounds": sum(round_stats) / len(round_stats) if round_stats else 0,
            "round_distribution": {
                "min": min(round_stats) if round_stats else 0,
                "max": max(round_stats) if round_stats else 0,
            },
        }

    def _find_master_tasks_file(self, domain: str = "medical") -> Optional[str]:
        final_domain = f"{domain}_general" if self.config.get("include_general", False) else domain
        master = os.path.join(self.output_dir, f"tasks_{final_domain}_total_{self.run_id}.jsonl")
        return master if os.path.exists(master) else None

    def batch_generate(
        self,
        domain: str,
        count: int = 5,
        max_workers: Optional[int] = None,
        include_general: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        max_workers = max_workers or self.max_workers
        if include_general is not None:
            self.config["include_general"] = include_general

        with self.stats_lock:
            self.stats.update({"total_tasks": count, "completed_tasks": 0, "failed_tasks": 0, "api_errors": 0, "start_time": time.time()})

        output_file = os.path.join(self.output_dir, "current_batch.jsonl")
        final_domain = f"{domain}_general" if self.config.get("include_general", False) else domain
        stats_file = os.path.join(self.output_dir, f"tasks_{final_domain}_summary_{self.run_id}.json")

        print(f"Generating {count} {domain} tasks using {max_workers} threads...")
        print(f"Output file: {output_file}")

        results: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._synthesize_single_task, domain, i) for i in range(count)]
            with tqdm(total=count, desc=f"{domain} task synthesis") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        results.append(result)
                        append_jsonl(result, output_file)
                    pbar.update(1)
                    with self.stats_lock:
                        pbar.set_postfix({
                            "completed": self.stats["completed_tasks"],
                            "failed": self.stats["failed_tasks"],
                            "rate": f"{self.stats['completed_tasks']}/{pbar.n}",
                        })
                    if pbar.n % self.save_frequency == 0:
                        master = self._find_master_tasks_file(domain)
                        self._save_stats(stats_file, master or output_file)

        master = self._find_master_tasks_file(domain)
        self._save_stats(stats_file, master or output_file)

        with self.stats_lock:
            success_rate = self.stats["completed_tasks"] / count * 100
            duration = time.time() - self.stats["start_time"]

        print(f"\nBatch generation completed!")
        print(f"Total tasks: {count}")
        print(f"Successful: {len(results)}")
        print(f"Failed: {self.stats['failed_tasks']}")
        print(f"Success rate: {success_rate:.1f}%")
        print(f"Duration: {duration:.1f}s")
        print(f"Results saved to: {output_file}")
        print(f"Statistics saved to: {stats_file}")

        return results
