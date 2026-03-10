"""
遗传疾病工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.medical.clinical_tables.genetic_diseases import GeneticDiseasesTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestGeneticDiseasesTool(VerifiableToolTestBase):
    """遗传疾病工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "GeneticDiseasesTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "terms": "cystic fibrosis",  # 搜索囊性纤维化相关疾病
            "count": 10,                 # 返回10个结果
            "offset": 0,                 # 从第0个开始
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return GeneticDiseasesTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx