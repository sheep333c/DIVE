"""Semantic Scholar数据集发布列表工具测试"""
from unittest.mock import MagicMock
from tools.academic.semantic_scholar.semantic_scholar_release_list import SemanticScholarReleaseListTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSemanticScholarReleaseListTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "SemanticScholarReleaseListTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {}

    def get_tool_instance(self):
        return SemanticScholarReleaseListTool()

    def get_execution_context(self):
        return self.mock_ctx
