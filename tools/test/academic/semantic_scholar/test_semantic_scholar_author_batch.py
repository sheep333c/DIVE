"""Semantic Scholar作者批量获取工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_author_batch import SemanticScholarAuthorBatchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarAuthorBatchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarAuthorBatchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"ids": ["1741101"]}

    def get_tool_instance(self):
        return SemanticScholarAuthorBatchTool()

    def get_execution_context(self):
        return self.mock_ctx
