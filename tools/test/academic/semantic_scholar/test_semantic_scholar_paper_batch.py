"""Semantic Scholar论文批量获取工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_paper_batch import SemanticScholarPaperBatchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarPaperBatchTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarPaperBatchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"ids": ["649def34f8be52c8b66281af98ae884c09aef38b"]}

    def get_tool_instance(self):
        return SemanticScholarPaperBatchTool()

    def get_execution_context(self):
        return self.mock_ctx
