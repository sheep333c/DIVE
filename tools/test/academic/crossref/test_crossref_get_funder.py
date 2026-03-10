"""Crossref Get Funder工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.academic.crossref.crossref_get_funder import CrossrefGetFunderTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCrossrefGetFunderTool(VerifiableToolTestBase):
    """Crossref Get Funder工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "CrossrefGetFunderTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 65000  # 65秒，比工具超时稍长
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "id": "10.13039/100000001"  # National Science Foundation
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CrossrefGetFunderTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
