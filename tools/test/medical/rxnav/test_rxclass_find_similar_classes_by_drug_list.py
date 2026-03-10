"""
RxclassFindSimilarClassesByDrugList工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxclass_find_similar_classes_by_drug_list import RxclassFindSimilarClassesByDrugListTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxclassFindSimilarClassesByDrugListTool(VerifiableToolTestBase):
    """根据药物列表查找相似Rxclass类别的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxclassFindSimilarClassesByDrugListTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxclassFindSimilarClassesByDrugListTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"rxcuis": "161 1191"}  # 使用正确的参数名和空格分隔格式
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxclassFindSimilarClassesByDrugListTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    