"""
RxnormFilterByProperty工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxnorm_filter_by_property import RxnormFilterByPropertyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxnormFilterByPropertyTool(VerifiableToolTestBase):
    """根据属性过滤Rxnorm概念的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxnormFilterByPropertyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxnormFilterByPropertyTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"rxcui": "161", "propName": "TTY", "propValues": "IN"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxnormFilterByPropertyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    