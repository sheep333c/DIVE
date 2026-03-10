#!/usr/bin/env python3
"""TaskSynthesizer minimal tests aligned with current implementation."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from dive.synthesizer import TaskSynthesizer
from dive.utils import retry_on_api_error


class _DummyRegistry:
    def create_tool(self, _tool_id):
        return object()


class _FakeToolRunner:
    def __init__(self):
        self.registry = _DummyRegistry()
        self._tool_name_mapping = {}

    def get_tool_descriptions(self, ids):
        return {}

    def get_tool_schemas(self, ids):
        return []

    def execute(self, name, inp):
        return "{}"

    def verify_tools(self, ids, domain):
        return ids, "0 tools"

    def get_domain_tool_ids(self, domain, include_general=False):
        return []

    def load_domain_tool_mapping(self):
        return {}


@pytest.fixture
def synthesizer(tmp_path, monkeypatch):
    import dive.tool_runner as tr_module
    monkeypatch.setattr(tr_module, "ToolRunner", _FakeToolRunner)
    return TaskSynthesizer(output_dir=str(tmp_path))


def test_retry_on_api_error_retries_then_succeeds():
    calls = {"n": 0}

    @retry_on_api_error(max_retries=3, delay=0, exponential_backoff=False)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise Exception("503 Service Unavailable")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_load_config_overrides_values(synthesizer, tmp_path):
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(
        yaml.safe_dump({"max_workers": 7, "temperature": 0.2}),
        encoding="utf-8",
    )

    cfg = synthesizer._load_config(str(cfg_file))
    assert cfg["max_workers"] == 7
    assert cfg["temperature"] == 0.2


def test_get_seed_returns_non_empty_string(synthesizer):
    seed = synthesizer.get_seed("medical")
    assert isinstance(seed, str)
    assert seed.strip() != ""


def test_parse_derivation_response_supports_query_answer(synthesizer):
    response = """QUERY: What is aspirin used for?
ANSWER: It is commonly used for pain and inflammation.
REASONING: Derived from collected evidence."""

    parsed = synthesizer._parse_derivation_response(response, strategy="test")
    assert "aspirin" in parsed["derived_question"].lower()
    assert "pain" in parsed["derived_answer"].lower()
    assert "evidence" in parsed["reasoning"].lower()
