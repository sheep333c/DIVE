"""Semantic Scholar论文标题搜索工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_paper_title_search import SemanticScholarPaperTitleSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarPaperTitleSearchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarPaperTitleSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"query": "Attention Is All You Need"}

    def get_tool_instance(self):
        return SemanticScholarPaperTitleSearchTool()

    def get_execution_context(self):
        return self.mock_ctx
