"""通用网页浏览工具测试"""
from unittest.mock import MagicMock
from tools.general.browse import GeneralBrowseTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestGeneralBrowseTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "GeneralBrowseTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"url": "https://example.com", "query": "example"}

    def get_tool_instance(self):
        return GeneralBrowseTool()

    def get_execution_context(self):
        return self.mock_ctx
