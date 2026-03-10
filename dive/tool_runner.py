#!/usr/bin/env python3
"""Tool execution layer — extracted from LLMClient."""

import json
from typing import Any, Dict, List, Optional, Set, Tuple

from .paths import (
    TOOLS_CONFIG_DIR,
    ensure_tools_on_path,
)


class ToolRunner:
    """Manages verifiable-tool registry, schema retrieval, and execution.

    The registry is loaded once and shared across all pipeline stages.
    All mappings are derived from the registry — no external JSON files needed.
    """

    def __init__(self) -> None:
        ensure_tools_on_path()
        from tools.core.registry import Registry

        self.registry = Registry.load(str(TOOLS_CONFIG_DIR))
        self._tool_name_mapping: Dict[str, str] = self._build_name_mapping()

    # ------------------------------------------------------------------
    # Mapping helpers (derived from registry)
    # ------------------------------------------------------------------

    def _build_name_mapping(self) -> Dict[str, str]:
        """Build {short_name: full_tool_id} from registry."""
        mapping: Dict[str, str] = {}
        for record in self.registry.list():
            short_name = record.id.split(".")[-1]
            mapping[short_name] = record.id
        return mapping

    def load_domain_tool_mapping(self) -> Dict[str, Dict[str, str]]:
        """Build {domain_tools: {short_name: full_id}} mapping from registry."""
        mapping: Dict[str, Dict[str, str]] = {}
        for record in self.registry.list():
            key = f"{record.domain}_tools"
            if key not in mapping:
                mapping[key] = {}
            short_name = record.id.split(".")[-1]
            mapping[key][short_name] = record.id
        return mapping

    def _get_general_tool_ids(self) -> Set[str]:
        """Get set of general-domain tool IDs from registry."""
        return {r.id for r in self.registry.list() if r.domain == "general"}

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def get_tool_schema(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get a single verifiable tool's schema in Claude API format."""
        try:
            record = self.registry.get(tool_id)
            if record is None:
                return None

            tool_real_name = tool_id.split(".")[-1]
            self._tool_name_mapping[tool_real_name] = tool_id

            return {
                "name": tool_real_name,
                "description": (record.description or "")[:500],
                "input_schema": record.input_schema or {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            }
        except Exception:
            return None

    def get_tool_schemas(self, tool_ids: List[str]) -> List[Dict[str, Any]]:
        """Get schemas for a list of tool IDs."""
        schemas: List[Dict[str, Any]] = []
        for tid in tool_ids:
            schema = self.get_tool_schema(tid)
            if schema:
                schemas.append(schema)
        return schemas

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a verifiable tool by short name."""
        try:
            from tools.core.runner import run_tool

            actual_tool_id = self._tool_name_mapping.get(tool_name)
            if not actual_tool_id:
                raise ValueError(f"Tool name '{tool_name}' not found in mapping")

            result = run_tool(self.registry, actual_tool_id, tool_input)
            if isinstance(result, dict):
                return json.dumps(result, ensure_ascii=False)
            return str(result)
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Verification / domain helpers
    # ------------------------------------------------------------------

    def verify_tools(self, tool_ids: List[str], domain: str) -> Tuple[List[str], str]:
        """Verify tool availability and return (verified_ids, stats_string)."""
        verified: List[str] = []
        domain_count = 0
        general_count = 0
        failed_count = 0

        base_domain = domain.removesuffix("_general")
        general_ids = self._get_general_tool_ids()

        for tid in tool_ids:
            try:
                self.registry.create_tool(tid)
                verified.append(tid)
                if tid in general_ids:
                    general_count += 1
                else:
                    domain_count += 1
            except Exception:
                failed_count += 1

        parts = []
        if domain_count:
            parts.append(f"{domain_count} {base_domain}")
        if general_count:
            parts.append(f"{general_count} general")
        if failed_count:
            parts.append(f"{failed_count} failed")
        stats = ", ".join(parts) if parts else "0 tools"

        return verified, stats

    def get_domain_tool_ids(self, domain: str, include_general: bool = False) -> List[str]:
        """Get verified tool IDs for a domain."""
        base_domain = domain.removesuffix("_general")

        available: List[str] = []
        for record in self.registry.list():
            if record.domain == base_domain:
                try:
                    self.registry.create_tool(record.id)
                    available.append(record.id)
                except Exception:
                    continue

        if include_general:
            for record in self.registry.list():
                if record.domain == "general":
                    try:
                        self.registry.create_tool(record.id)
                        available.append(record.id)
                    except Exception:
                        continue

        return available

    def get_tool_descriptions(self, tool_ids: List[str]) -> Dict[str, str]:
        """Get tool_name → description mapping for the given IDs."""
        descriptions: Dict[str, str] = {}
        for tid in tool_ids:
            tool_name = tid.split(".")[-1]
            record = self.registry.get(tid)
            if record and record.description:
                descriptions[tool_name] = record.description[:200]
            else:
                descriptions[tool_name] = tid
        return descriptions
