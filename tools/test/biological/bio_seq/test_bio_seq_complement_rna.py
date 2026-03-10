"""Bio.Seq RNA互补工具测试"""
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_complement_rna import BioSeqComplementRnaTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqComplementRnaTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqComplementRnaTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"sequence": "AUCG"}

    def get_tool_instance(self):
        return BioSeqComplementRnaTool()

    def get_execution_context(self):
        return self.mock_ctx
