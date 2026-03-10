"""
Code execution tool for tools.

Executes code in a sandboxed environment via SandboxFusion.
Uses Jupyter mode (/run_jupyter) by default for better output capture.
"""

import json
import os
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from .utils.code_sandbox_utils import get_code_sandbox_client


class CodeExecutionTool(Tool):
    """
    Tool for code execution in a sandboxed environment.

    Input Parameters:
        - code (str, required): Code to execute

    Output Format:
        Returns string representation of execution results.
        Example: "{'status': 'Finished', 'return_code': 0, 'stdout': 'Hello\\n', 'stderr': ''}"
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """Execute code in sandbox using Jupyter mode."""
        try:
            code = params.get("code", "")
            if not code.strip():
                return {"error": "Code parameter is required and cannot be empty"}

            client = get_code_sandbox_client()
            success, result = client.run_jupyter([code])
            return str(result)

        except Exception as e:
            return {"error": f"Code execution failed: {e}"}
# Backwards-compatible alias
GeneralCodeSandboxTool = CodeExecutionTool
