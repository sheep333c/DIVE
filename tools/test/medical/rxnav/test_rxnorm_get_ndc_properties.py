"""
RxnormGetNdcProperties工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxnorm_get_ndc_properties import RxnormGetNdcPropertiesTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxnormGetNdcPropertiesTool(VerifiableToolTestBase):
    """获取Rxnorm NDC属性的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxnormGetNdcPropertiesTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxnormGetNdcPropertiesTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"id": "0378-3950-07"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxnormGetNdcPropertiesTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    