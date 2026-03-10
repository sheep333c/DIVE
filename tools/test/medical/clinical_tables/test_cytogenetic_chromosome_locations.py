"""
细胞遗传学染色体位置工具测试
继承VerifiableToolTestBase，获得完整的测试覆盖
"""
import unittest
from unittest.mock import MagicMock

from tools.medical.clinical_tables.cytogenetic_chromosome_locations import CytogeneticChromosomeLocationsTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCytogeneticChromosomeLocationsTool(VerifiableToolTestBase):
    """
    细胞遗传学染色体位置搜索工具测试
    """
    __test__ = True
    TOOL_CLASS_NAME = "CytogeneticChromosomeLocationsTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = CytogeneticChromosomeLocationsTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    # 实现基类抽象方法
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "terms": "1p36",        # 搜索1号染色体短臂特定区域
            "count": 15,            # 返回15个结果（分页大小）
            "offset": 0,            # 从第0个开始（0-based）
            "df": "cytogenetic",    # 显示字段：细胞遗传学位置
            "cf": "cytogenetic"     # 代码字段：细胞遗传学位置
        }
    
    def get_tool_instance(self):
        return self.tool
    
    def get_execution_context(self):
        return self.mock_ctx
    

if __name__ == '__main__':
    unittest.main()