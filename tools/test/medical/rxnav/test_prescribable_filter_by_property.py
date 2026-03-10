"""
按属性过滤可处方概念的工具测试
基于配置文件中的工具信息，严格对应实现
"""
import unittest
from unittest.mock import MagicMock

from tools.medical.rxnav.prescribable_filter_by_property import PrescribableFilterByPropertyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestPrescribableFilterByPropertyTool(VerifiableToolTestBase):
    """按属性过滤可处方概念的工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "PrescribableFilterByPropertyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = PrescribableFilterByPropertyTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"rxcui": "7052", "propName": "TTY", "propValues": "IN PIN"}
    
    def get_tool_instance(self):
        return self.tool
    
    def get_execution_context(self):
        return self.mock_ctx
    

if __name__ == '__main__':
    unittest.main()