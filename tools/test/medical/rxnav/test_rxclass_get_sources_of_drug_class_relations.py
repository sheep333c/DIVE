"""
RxclassGetSourcesOfDrugClassRelations工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxclass_get_sources_of_drug_class_relations import RxclassGetSourcesOfDrugClassRelationsTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxclassGetSourcesOfDrugClassRelationsTool(VerifiableToolTestBase):
    """获取药物类别关系源的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxclassGetSourcesOfDrugClassRelationsTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxclassGetSourcesOfDrugClassRelationsTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxclassGetSourcesOfDrugClassRelationsTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    