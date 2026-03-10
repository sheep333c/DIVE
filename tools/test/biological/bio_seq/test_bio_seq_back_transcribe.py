"""Bio.Seq反转录工具测试"""
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_back_transcribe import BioSeqBackTranscribeTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqBackTranscribeTool(VerifiableToolTestBase):
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqBackTranscribeTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {"sequence": "AUCG"}

    def get_tool_instance(self):
        return BioSeqBackTranscribeTool()

    def get_execution_context(self):
        return self.mock_ctx
