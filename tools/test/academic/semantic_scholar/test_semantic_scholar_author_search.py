"""Semantic Scholar作者搜索工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_author_search import SemanticScholarAuthorSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarAuthorSearchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarAuthorSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"query": "Yann LeCun", "limit": 3}

    def get_tool_instance(self):
        return SemanticScholarAuthorSearchTool()

    def get_execution_context(self):
        return self.mock_ctx
