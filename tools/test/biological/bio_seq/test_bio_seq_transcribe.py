"""
Bio.Seq Transcribe工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_transcribe import BioSeqTranscribeTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqTranscribeTool(VerifiableToolTestBase):
    """Bio.Seq Transcribe工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "BioSeqTranscribeTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于测试的参数"""
        return {
            "sequence": "ATCG",
            "operation": "transcribe"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return BioSeqTranscribeTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx