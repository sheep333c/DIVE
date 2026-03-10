"""
RxclassGetClassContexts工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxclass_get_class_contexts import RxclassGetClassContextsTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxclassGetClassContextsTool(VerifiableToolTestBase):
    """获取Rxclass类别上下文的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxclassGetClassContextsTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxclassGetClassContextsTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"classId": "N0000175659"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxclassGetClassContextsTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    