"""
NCBI Entrez数据库信息工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.biological.ncbi_entrez.ncbi_entrez_einfo import NcbiEntrezEinfoTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestNcbiEntrezEinfoTool(VerifiableToolTestBase):
    """NCBI Entrez数据库信息工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "NcbiEntrezEinfoTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "db": "pubmed",
            "version": "2.0"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return NcbiEntrezEinfoTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx