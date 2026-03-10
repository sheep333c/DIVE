"""Semantic Scholar论文参考文献工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_paper_references import SemanticScholarPaperReferencesTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarPaperReferencesTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarPaperReferencesTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"paper_id": "649def34f8be52c8b66281af98ae884c09aef38b", "limit": 3}

    def get_tool_instance(self):
        return SemanticScholarPaperReferencesTool()

    def get_execution_context(self):
        return self.mock_ctx
