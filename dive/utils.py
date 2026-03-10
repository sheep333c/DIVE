#!/usr/bin/env python3
"""Shared utility functions for the DIVE pipeline."""

import glob
import json
import os
import time
import threading
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional

# Module-level lock for append_jsonl thread safety
_jsonl_write_lock = threading.Lock()


def extract_run_id(output_dir: str) -> str:
    """Extract run_id (YYYYMMDD_HHMMSS) from an output directory path.

    """
    try:
        parts = output_dir.split(os.sep)
        for part in parts:
            if (
                len(part) == 15
                and part[8] == "_"
                and part[:8].isdigit()
                and part[9:].isdigit()
            ):
                return part
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    except Exception:
        return datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------------------------
# JSONL I/O
# ---------------------------------------------------------------------------

def load_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """Load a JSONL file and return a list of records."""
    results: List[Dict[str, Any]] = []
    if not file_path or not os.path.exists(file_path):
        return results
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return results


def load_jsonl_by_uuid(file_path: str) -> Dict[str, Dict[str, Any]]:
    """Load a JSONL file keyed by uuid field."""
    data: Dict[str, Dict[str, Any]] = {}
    if not file_path or not os.path.exists(file_path):
        return data
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    uuid_key = record.get("uuid")
                    if uuid_key:
                        data[uuid_key] = record
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")
    return data


def append_jsonl(record: Dict[str, Any], output_file: str) -> None:
    """Append a single JSON record to a JSONL file (thread-safe)."""
    with _jsonl_write_lock:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Warning: Save failed: {e}")


def write_json(data: Any, file_path: str) -> None:
    """Write JSON data to a file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Warning: JSON write failed: {e}")


# ---------------------------------------------------------------------------
# File finding
# ---------------------------------------------------------------------------

def find_latest_glob(base_dir: str, pattern: str) -> Optional[str]:
    """Find the latest file matching a glob pattern in base_dir."""
    files = glob.glob(os.path.join(base_dir, pattern))
    if files:
        return max(files, key=os.path.getmtime)
    return None


def find_input_file(input_dir: str, current_name: str, pattern: str) -> Optional[str]:
    """Find an input file — prefer current_name, fallback to glob pattern."""
    current_file = Path(input_dir) / current_name
    if current_file.exists():
        return str(current_file)
    files = glob.glob(os.path.join(input_dir, pattern))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def count_lines_in_file(file_path: str) -> int:
    """Count non-empty lines in a file."""
    if not file_path or not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Retry decorator
# ---------------------------------------------------------------------------

def retry_on_api_error(max_retries: int = 3, delay: int = 30, exponential_backoff: bool = True):
    """API error retry decorator with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    error_str = str(e).lower()
                    if any(kw in error_str for kw in ["503", "exceeded", "rate_limit", "too many requests"]):
                        if attempt < max_retries - 1:
                            wait_time = delay * (2 ** attempt if exponential_backoff else 1)
                            print(f"API rate limit error (attempt {attempt + 1}), waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                    raise e
            raise last_exception
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Pipeline base class
# ---------------------------------------------------------------------------

from abc import ABC


class PipelineStage(ABC):
    """Common base for every pipeline stage (synthesizer, solver, verifier, aggregator)."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    @property
    def run_id(self) -> str:
        return getattr(self, "_run_id_override", None) or extract_run_id(self.output_dir)

    @run_id.setter
    def run_id(self, value: str) -> None:
        self._run_id_override = value

    @property
    def current_batch_file(self) -> Path:
        return Path(self.output_dir) / "current_batch.jsonl"
