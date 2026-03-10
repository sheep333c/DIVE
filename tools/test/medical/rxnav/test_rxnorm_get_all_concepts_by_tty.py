"""
RxnormGetAllConceptsByTty工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxnorm_get_all_concepts_by_tty import RxnormGetAllConceptsByTtyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxnormGetAllConceptsByTtyTool(VerifiableToolTestBase):
    """根据术语类型获取所有Rxnorm概念的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxnormGetAllConceptsByTtyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxnormGetAllConceptsByTtyTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"tty": "IN"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxnormGetAllConceptsByTtyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
