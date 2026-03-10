"""
RxnormGetNdcs工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxnorm_get_ndcs import RxnormGetNdcsTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxnormGetNdcsTool(VerifiableToolTestBase):
    """获取Rxnorm NDC的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxnormGetNdcsTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxnormGetNdcsTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"rxcui": "617312"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxnormGetNdcsTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    