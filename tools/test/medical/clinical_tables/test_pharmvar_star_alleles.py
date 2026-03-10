"""
PharmVar星号等位基因工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.medical.clinical_tables.pharmvar_star_alleles import PharmvarStarAllelesTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestPharmvarStarAllelesTool(VerifiableToolTestBase):
    """PharmVar星号等位基因工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "PharmvarStarAllelesTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "terms": "CYP2D6",           # 搜索CYP2D6基因的星号等位基因
            "count": 10,                 # 返回10个结果
            "offset": 0,                 # 从第0个开始
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return PharmvarStarAllelesTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx