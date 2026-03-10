"""Semantic Scholar论文搜索工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_paper_search import SemanticScholarPaperSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarPaperSearchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarPaperSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"query": "machine learning", "limit": 3}

    def get_tool_instance(self):
        return SemanticScholarPaperSearchTool()

    def get_execution_context(self):
        return self.mock_ctx
