"""代码执行工具测试"""
from unittest.mock import MagicMock
from tools.general.code_execution import CodeExecutionTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCodeExecutionTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "CodeExecutionTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"code": "print(1 + 1)"}

    def get_tool_instance(self):
        return CodeExecutionTool()

    def get_execution_context(self):
        return self.mock_ctx
