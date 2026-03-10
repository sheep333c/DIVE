"""Semantic Scholar作者论文工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_author_papers import SemanticScholarAuthorPapersTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarAuthorPapersTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarAuthorPapersTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"author_id": "1741101", "limit": 3}

    def get_tool_instance(self):
        return SemanticScholarAuthorPapersTool()

    def get_execution_context(self):
        return self.mock_ctx
