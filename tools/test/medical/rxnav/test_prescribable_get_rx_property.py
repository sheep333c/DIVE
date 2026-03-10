"""
PrescribableGetRxProperty工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.prescribable_get_rx_property import PrescribableGetRxPropertyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestPrescribableGetRxPropertyTool(VerifiableToolTestBase):
    """获取可处方Rxnorm属性的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "PrescribableGetRxPropertyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = PrescribableGetRxPropertyTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"rxcui": "131725", "propName": "RxNorm Name"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return PrescribableGetRxPropertyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    