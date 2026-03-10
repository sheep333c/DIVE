"""
通过ID查找可处方RxCUI的工具测试
基于配置文件中的工具信息，严格对应实现
"""
import unittest
from unittest.mock import MagicMock

from tools.medical.rxnav.prescribable_find_rxcui_by_id import PrescribableFindRxcuiByIdTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestPrescribableFindRxcuiByIdTool(VerifiableToolTestBase):
    """通过ID查找可处方RxCUI的工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "PrescribableFindRxcuiByIdTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"idtype": "NDC", "id": "0378-3950-07"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return PrescribableFindRxcuiByIdTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    