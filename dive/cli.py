#!/usr/bin/env python3
"""Unified CLI for the DIVE pipeline.

Usage:
    dive --config dive.yaml synthesize   # Generate tasks only
    dive --config dive.yaml end2end      # Full pipeline: synthesize → solve → verify → aggregate
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .aggregator import TaskAggregator
from .synthesizer import TaskSynthesizer
from .solver import TaskSolver
from .verifier import TaskVerifier
from .tool_runner import ToolRunner
from .utils import find_input_file, load_jsonl, write_json

try:
    import yaml
except ImportError:
    yaml = None


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

_DEFAULTS: Dict[str, Any] = {
    "domain": "medical",
    "workers": 4,
    "count": 100,
    "batch_size": 20,
    "include_general": False,
    "base_dir": "output",
    "delay_strategy": "progressive",
}

# yaml "api_keys" → environment variables
_API_KEY_ENV_MAP = {
    "anthropic_api_key": "ANTHROPIC_API_KEY",
    "anthropic_base_url": "ANTHROPIC_BASE_URL",
    "llm_provider": "LLM_PROVIDER",
    "serper_api_key": "SERPER_API_KEY",
    "jina_api_key": "JINA_API_KEY",
    "browse_llm_api_key": "BROWSE_LLM_API_KEY",
    "browse_llm_base_url": "BROWSE_LLM_BASE_URL",
    "browse_llm_model": "BROWSE_LLM_MODEL",
    "tushare_token": "TUSHARE_TOKEN",
    "sandbox_fusion_url": "SANDBOX_FUSION_URL",
    "semantic_scholar_api_key": "SEMANTIC_SCHOLAR_API_KEY",
    "ncbi_api_key": "NCBI_API_KEY",
    "ncbi_email": "NCBI_EMAIL",
}


def _load_config(config_path: Optional[str]) -> Dict[str, Any]:
    if not config_path:
        return {}
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        return json.loads(text) or {}
    if suffix in (".yaml", ".yml"):
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML config files")
        return yaml.safe_load(text) or {}
    # Try yaml first, then json
    if yaml is not None:
        try:
            return yaml.safe_load(text) or {}
        except Exception:
            pass
    return json.loads(text) or {}


def _apply_api_keys(config: Dict[str, Any]) -> None:
    """Set api_keys from config as environment variables (won't overwrite existing)."""
    keys_section = config.get("api_keys", {})
    if not isinstance(keys_section, dict):
        return
    for yaml_key, env_var in _API_KEY_ENV_MAP.items():
        value = keys_section.get(yaml_key)
        if value and not os.getenv(env_var):
            os.environ[env_var] = str(value)


def _cfg(config: Dict[str, Any], key: str) -> Any:
    """Get a config value: pipeline section → top-level → default."""
    pipeline_cfg = config.get("pipeline", {}) or {}
    if key in pipeline_cfg:
        return pipeline_cfg[key]
    if key in config:
        return config[key]
    return _DEFAULTS.get(key)


def _build_llm_config(config: Dict[str, Any], stage: str,
                      args: Optional[argparse.Namespace] = None) -> Dict[str, Any]:
    """Build LLM config for a stage (synthesizer/solver/verifier).

    Priority: CLI args > yaml pipeline section > empty (falls back to env vars in LLMClient).
    """
    pipeline_cfg = config.get("pipeline", {}) or {}
    cfg: Dict[str, Any] = {}
    for key in ("api_key", "base_url", "model", "provider"):
        # CLI arg takes priority
        cli_val = getattr(args, f"{stage}_{key}", None) if args else None
        val = cli_val or pipeline_cfg.get(f"{stage}_{key}")
        if val:
            cfg[key] = val
    return cfg


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _final_domain(domain: str, include_general: bool) -> str:
    return f"{domain}_general" if include_general else domain


def _batch_size_for_index(total: int, batch_size: int, idx: int, total_batches: int) -> int:
    if idx == total_batches:
        return total - (idx - 1) * batch_size
    return batch_size


def _append_jsonl(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Batch output not found: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(src, "r", encoding="utf-8") as f_src, open(dst, "a", encoding="utf-8") as f_dst:
        for line in f_src:
            f_dst.write(line)


# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

def _run(config: Dict[str, Any], mode: str, args: argparse.Namespace) -> None:
    """Core pipeline runner for both 'synthesize' and 'end2end' modes."""
    # CLI args override yaml config
    domain = args.domain or _cfg(config, "domain")
    workers = int(args.workers or _cfg(config, "workers"))
    count = int(args.count or _cfg(config, "count"))
    batch_size = int(args.batch_size or _cfg(config, "batch_size"))
    include_general = args.include_general or bool(_cfg(config, "include_general"))
    base_dir_str = args.base_dir or str(_cfg(config, "base_dir"))
    delay_strategy = getattr(args, "delay_strategy", None) or str(_cfg(config, "delay_strategy"))
    run_id = args.run_id or _cfg(config, "run_id") or datetime.now().strftime("%Y%m%d_%H%M%S")

    do_solve = mode == "end2end"
    do_verify = mode == "end2end"
    do_aggregate = mode == "end2end"

    final_domain = _final_domain(domain, include_general)
    base_dir = Path(base_dir_str) / run_id
    tasks_dir = base_dir / "tasks"
    trajectories_dir = base_dir / "trajectories"
    verifications_dir = base_dir / "verifications"
    final_dir = base_dir / "final"
    for d in [tasks_dir, trajectories_dir, verifications_dir, final_dir]:
        d.mkdir(parents=True, exist_ok=True)

    tool_runner = ToolRunner()

    total_tasks = tasks_dir / f"tasks_{final_domain}_total_{run_id}.jsonl"
    total_trajectories = trajectories_dir / f"trajectories_{final_domain}_total_{run_id}.jsonl"
    total_verifications = verifications_dir / f"verifications_total_{run_id}.jsonl"

    total_batches = (count + batch_size - 1) // batch_size
    print(f"[{mode}] run_id={run_id}, total={count}, batches={total_batches}, domain={final_domain}")

    syn_llm = _build_llm_config(config, "synthesizer", args)
    sol_llm = _build_llm_config(config, "solver", args)
    ver_llm = _build_llm_config(config, "verifier", args)

    for i in range(1, total_batches + 1):
        current_count = _batch_size_for_index(count, batch_size, i, total_batches)

        # Clean up batch files from previous iteration
        for p in [tasks_dir / "current_batch.jsonl", trajectories_dir / "current_batch.jsonl",
                   verifications_dir / "current_batch.jsonl"]:
            if p.exists():
                p.unlink()

        # --- Synthesize ---
        print(f"[Batch {i}/{total_batches}] generating {current_count} tasks")
        synthesizer = TaskSynthesizer(
            output_dir=str(tasks_dir), tool_runner=tool_runner, llm_config=syn_llm,
        )
        synthesizer.batch_generate(
            domain=domain, count=current_count, max_workers=workers,
            include_general=include_general,
        )
        _append_jsonl(tasks_dir / "current_batch.jsonl", total_tasks)

        # --- Solve ---
        if do_solve:
            print(f"[Batch {i}/{total_batches}] solving tasks")
            task_file = find_input_file(str(tasks_dir), "current_batch.jsonl", "tasks_*.jsonl")
            if task_file:
                solver = TaskSolver(
                    output_dir=str(trajectories_dir), tool_runner=tool_runner, llm_config=sol_llm,
                )
                solver.solve_task_file(task_file, final_domain, workers)
                _append_jsonl(trajectories_dir / "current_batch.jsonl", total_trajectories)

        # --- Verify ---
        if do_verify:
            print(f"[Batch {i}/{total_batches}] verifying trajectories")
            traj_file = find_input_file(str(trajectories_dir), "current_batch.jsonl", "trajectories_*.jsonl")
            if traj_file:
                verifier = TaskVerifier(
                    output_dir=str(verifications_dir), delay_strategy=delay_strategy,
                    llm_config=ver_llm,
                )
                verifier.verify_trajectory_file(traj_file, workers, final_domain)
                _append_jsonl(verifications_dir / "current_batch.jsonl", total_verifications)

        # --- Aggregate ---
        if do_aggregate:
            print(f"[Batch {i}/{total_batches}] aggregating")
            aggregator = TaskAggregator(output_dir=str(final_dir))
            aggregator.aggregate_results(
                tasks_file=str(total_tasks),
                trajectories_file=str(total_trajectories) if total_trajectories.exists() else None,
                verifications_file=str(total_verifications) if total_verifications.exists() else None,
                auto_find=False,
            )

    # --- Final summaries ---
    if total_tasks.exists():
        syn = TaskSynthesizer(output_dir=str(tasks_dir), tool_runner=tool_runner)
        syn.run_id = run_id
        syn._save_stats(
            str(tasks_dir / f"tasks_{final_domain}_summary_{run_id}.json"),
            str(total_tasks),
        )

    if do_solve and total_trajectories.exists():
        total_task_count = len(list(load_jsonl(str(total_tasks)))) if total_tasks.exists() else 0
        sol = TaskSolver(output_dir=str(trajectories_dir), tool_runner=tool_runner)
        sol.run_id = run_id
        sol._save_trajectory_stats(
            str(total_trajectories),
            str(trajectories_dir / f"trajectories_{final_domain}_summary_{run_id}.json"),
            total_task_count,
        )

    if do_verify and total_verifications.exists():
        ver = TaskVerifier(output_dir=str(verifications_dir))
        ver.run_id = run_id
        summary_stats = ver._calculate_verification_stats_from_file(
            str(total_verifications),
            str(total_trajectories) if total_trajectories.exists() else "",
        )
        write_json(summary_stats, str(verifications_dir / f"verifications_{final_domain}_summary_{run_id}.json"))

    print(f"Pipeline finished. Outputs at {base_dir}")


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

def _parse_bootstrap_args() -> argparse.Namespace:
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument("--config", default=None)
    args, _ = bootstrap.parse_known_args()
    return args


def _add_llm_args(parser: argparse.ArgumentParser, prefix: str) -> None:
    """Add --{prefix}_api_key, --{prefix}_base_url, --{prefix}_model, --{prefix}_provider."""
    parser.add_argument(f"--{prefix}_api_key", default=None, help=f"API key for {prefix}")
    parser.add_argument(f"--{prefix}_base_url", default=None, help=f"API base URL for {prefix}")
    parser.add_argument(f"--{prefix}_model", default=None, help=f"Model for {prefix}")
    parser.add_argument(f"--{prefix}_provider", default=None,
                        choices=["anthropic", "openai_compatible"], help=f"LLM provider for {prefix}")


def _add_common_args(parser: argparse.ArgumentParser, cfg: Dict) -> None:
    """Add common pipeline args to a subcommand parser."""
    parser.add_argument("--domain", default=None)
    parser.add_argument("--count", type=int, default=None)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--batch_size", type=int, default=None)
    parser.add_argument("--include_general", action="store_true", default=None)
    parser.add_argument("--base_dir", default=None)
    parser.add_argument("--run_id", default=None)


def build_parser(runtime_cfg: Optional[Dict] = None) -> argparse.ArgumentParser:
    runtime_cfg = runtime_cfg or {}
    parser = argparse.ArgumentParser(prog="dive", description="DIVE pipeline CLI")
    parser.add_argument("--config", default=None, help="YAML/JSON config file")
    sub = parser.add_subparsers(dest="command", required=True)

    p_synth = sub.add_parser("synthesize", help="Generate tasks only")
    _add_common_args(p_synth, runtime_cfg)
    _add_llm_args(p_synth, "synthesizer")

    p_e2e = sub.add_parser("end2end", help="Full pipeline: synthesize → solve → verify → aggregate")
    _add_common_args(p_e2e, runtime_cfg)
    p_e2e.add_argument("--delay_strategy", default=None, choices=["none", "progressive", "random"])
    _add_llm_args(p_e2e, "synthesizer")
    _add_llm_args(p_e2e, "solver")
    _add_llm_args(p_e2e, "verifier")

    return parser


def main() -> None:
    bootstrap_args = _parse_bootstrap_args()
    runtime_cfg = _load_config(bootstrap_args.config)
    _apply_api_keys(runtime_cfg)
    parser = build_parser(runtime_cfg)
    args = parser.parse_args()
    _run(runtime_cfg, mode=args.command, args=args)


if __name__ == "__main__":
    main()
