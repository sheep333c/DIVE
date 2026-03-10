"""通用并行搜索工具测试"""
from unittest.mock import MagicMock
from tools.general.parallel_search import GeneralParallelSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestGeneralParallelSearchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "GeneralParallelSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"queries": ["machine learning", "deep learning"]}

    def get_tool_instance(self):
        return GeneralParallelSearchTool()

    def get_execution_context(self):
        return self.mock_ctx
