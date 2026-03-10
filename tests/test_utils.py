#!/usr/bin/env python3
"""Tests for dive.utils."""

import json
import os

import pytest

from dive.utils import (
    append_jsonl,
    count_lines_in_file,
    extract_run_id,
    find_input_file,
    find_latest_glob,
    load_jsonl,
    load_jsonl_by_uuid,
    retry_on_api_error,
    write_json,
)


class TestExtractRunId:
    def test_extracts_timestamp_from_path(self):
        assert extract_run_id("results/20250101_120000/tasks") == "20250101_120000"

    def test_fallback_when_no_timestamp(self):
        rid = extract_run_id("results/some_dir")
        assert len(rid) == 15 and rid[8] == "_"


class TestJsonlIO:
    def test_load_jsonl(self, tmp_path):
        f = tmp_path / "test.jsonl"
        f.write_text('{"a":1}\n{"b":2}\n', encoding="utf-8")
        records = load_jsonl(str(f))
        assert len(records) == 2
        assert records[0]["a"] == 1

    def test_load_jsonl_missing_file(self):
        assert load_jsonl("/nonexistent/file.jsonl") == []

    def test_load_jsonl_by_uuid(self, tmp_path):
        f = tmp_path / "test.jsonl"
        f.write_text('{"uuid":"aaa","x":1}\n{"uuid":"bbb","x":2}\n', encoding="utf-8")
        data = load_jsonl_by_uuid(str(f))
        assert "aaa" in data
        assert data["bbb"]["x"] == 2

    def test_append_jsonl(self, tmp_path):
        f = tmp_path / "out.jsonl"
        append_jsonl({"k": "v1"}, str(f))
        append_jsonl({"k": "v2"}, str(f))
        lines = f.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2

    def test_write_json(self, tmp_path):
        f = tmp_path / "out.json"
        write_json({"hello": "world"}, str(f))
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data["hello"] == "world"


class TestFindFiles:
    def test_find_latest_glob(self, tmp_path):
        (tmp_path / "a_001.jsonl").write_text("{}")
        (tmp_path / "a_002.jsonl").write_text("{}")
        result = find_latest_glob(str(tmp_path), "a_*.jsonl")
        assert result is not None
        assert "a_002" in result

    def test_find_latest_glob_no_match(self, tmp_path):
        assert find_latest_glob(str(tmp_path), "*.xyz") is None

    def test_find_input_file_prefers_current(self, tmp_path):
        (tmp_path / "current_batch.jsonl").write_text("{}")
        result = find_input_file(str(tmp_path), "current_batch.jsonl", "tasks_*.jsonl")
        assert "current_batch" in result

    def test_count_lines(self, tmp_path):
        f = tmp_path / "data.jsonl"
        f.write_text("line1\nline2\n\nline3\n", encoding="utf-8")
        assert count_lines_in_file(str(f)) == 3


class TestRetryDecorator:
    def test_succeeds_immediately(self):
        @retry_on_api_error(max_retries=3, delay=0)
        def ok():
            return 42
        assert ok() == 42

    def test_retries_on_rate_limit(self):
        calls = {"n": 0}

        @retry_on_api_error(max_retries=3, delay=0, exponential_backoff=False)
        def flaky():
            calls["n"] += 1
            if calls["n"] < 2:
                raise Exception("rate_limit exceeded")
            return "done"

        assert flaky() == "done"
        assert calls["n"] == 2

    def test_raises_non_retryable(self):
        @retry_on_api_error(max_retries=3, delay=0)
        def fail():
            raise ValueError("bad input")

        with pytest.raises(ValueError):
            fail()
