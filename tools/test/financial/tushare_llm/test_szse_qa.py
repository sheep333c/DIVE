"""
深证易互动问答工具测试
"""
import unittest
from unittest.mock import MagicMock
from tools.financial.tushare_llm.szse_qa import SzseQaTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestSzseQaTool(VerifiableToolTestBase):
    """深证易互动问答工具测试类"""
    __test__ = True
    TOOL_CLASS_NAME = "SzseQaTool"
    
    def get_tool_instance(self):
        """获取工具实例"""
        return SzseQaTool()
    
    def get_test_params(self):
        """获取测试参数"""
        return {
            'ts_code': '000001.SZ',
            'start_date': '20240101',
            'end_date': '20240131'
        }
    
    def setUp(self):
        """测试设置"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
        self.tool = self.get_tool_instance()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()