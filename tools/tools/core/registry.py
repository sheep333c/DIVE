from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from .tool import Tool
from .types import ToolDescriptor


@dataclass
class ToolRecord:
    id: str
    domain: str
    version: str
    description: str
    module: str  # e.g., "medical.icd.icd10cm_search:ICD10CMSearchTool"
    input_schema: Optional[Dict[str, Any]]
    output_schema: Optional[Dict[str, Any]]
    meta: Dict[str, Any]
    auth: Dict[str, Any]


class Registry:
    def __init__(self, tools: Dict[str, ToolRecord]):
        self._tools = tools

    @classmethod
    def load(cls, root_dir: str) -> "Registry":
        tools: Dict[str, ToolRecord] = {}
        for path in _iter_manifest_paths(root_dir):
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Support grouped tool configs and legacy tools format
            processed_any_group = False
            
            # Check for grouped formats (e.g., "clinical_tables", "rxnav", etc.)
            for group_key, group_tools in config.items():
                if group_key != "tools" and isinstance(group_tools, list):
                    processed_any_group = True
                    for manifest in group_tools:
                        record = ToolRecord(
                            id=manifest["id"],
                            domain=manifest["domain"],
                            version=manifest.get("version", "0.1.0"),
                            description=manifest.get("description", ""),
                            module=manifest["module"],
                            input_schema=manifest.get("input_schema") or manifest.get("parameters"),
                            output_schema=manifest.get("output_schema"),
                            meta=manifest.get("meta", {}),
                            auth=manifest.get("auth", {}),
                        )
                        tools[record.id] = record
            
            # Legacy format: tools array
            if not processed_any_group and "tools" in config:
                for manifest in config["tools"]:
                    record = ToolRecord(
                        id=manifest["id"],
                        domain=manifest["domain"],
                        version=manifest.get("version", "0.1.0"),
                        description=manifest.get("description", ""),
                        module=manifest["module"],
                        input_schema=manifest.get("input_schema") or manifest.get("parameters"),
                        output_schema=manifest.get("output_schema"),
                        meta=manifest.get("meta", {}),
                        auth=manifest.get("auth", {}),
                    )
                    tools[record.id] = record
                    
            # Old format: single tool manifest (fallback)
            if not processed_any_group and "tools" not in config:
                if "id" in config and "module" in config:
                    record = ToolRecord(
                        id=config["id"],
                        domain=config["domain"],
                        version=config.get("version", "0.1.0"),
                        description=config.get("description", ""),
                        module=config["module"],
                        input_schema=config.get("input_schema"),
                        output_schema=config.get("output_schema"),
                        meta=config.get("meta", {}),
                        auth=config.get("auth", {}),
                    )
                    tools[record.id] = record
        return cls(tools)

    def get(self, tool_id: str) -> Optional[ToolRecord]:
        return self._tools.get(tool_id)

    def list(self) -> Iterable[ToolRecord]:
        return self._tools.values()

    def create_tool(self, tool_id: str) -> Tool:
        record = self.get(tool_id)
        if record is None:
            raise KeyError(f"Tool not found: {tool_id}")
        module_path, _, class_name = record.module.partition(":")
        if not module_path or not class_name:
            raise ValueError(f"Invalid module spec for tool {tool_id}: {record.module}")
        module = importlib.import_module(module_path)
        cls_obj = getattr(module, class_name)
        tool: Tool = cls_obj()
        # Fill descriptor from manifest
        tool.descriptor = ToolDescriptor(
            id=record.id,
            domain=record.domain,
            version=record.version,
            description=record.description,
            auth=record.auth,
            input_schema=record.input_schema,
            output_schema=record.output_schema,
            meta=record.meta,
        )
        return tool


def _iter_manifest_paths(root_dir: str):
    # Look for config files in configs directories first
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        if "configs" in dirpath:
            for name in filenames:
                if name.endswith(".json"):
                    yield os.path.join(dirpath, name)
    
    # Also support old format for backward compatibility
    for dirpath, _dirnames, filenames in os.walk(root_dir):
        if "configs" not in dirpath:
            for name in filenames:
                if name == "manifest.json" or name.endswith(".manifest.json"):
                    yield os.path.join(dirpath, name)







