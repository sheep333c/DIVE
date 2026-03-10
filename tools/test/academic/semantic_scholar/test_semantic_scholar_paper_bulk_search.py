"""Semantic Scholar论文批量搜索工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_paper_bulk_search import SemanticScholarPaperBulkSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarPaperBulkSearchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarPaperBulkSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"query": "deep learning"}

    def get_tool_instance(self):
        return SemanticScholarPaperBulkSearchTool()

    def get_execution_context(self):
        return self.mock_ctx
