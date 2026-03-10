"""
新闻联播文字稿工具测试
"""
import unittest
from unittest.mock import MagicMock
from tools.financial.tushare_llm.news_cctv import NewsCctvTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestNewsCctvTool(VerifiableToolTestBase):
    """新闻联播文字稿工具测试类"""
    __test__ = True
    TOOL_CLASS_NAME = "NewsCctvTool"
    
    def get_tool_instance(self):
        """获取工具实例"""
        return NewsCctvTool()
    
    def get_test_params(self):
        """获取测试参数"""
        return {
            'date': '20240101',
            'start_date': '20240101',
            'end_date': '20240107'
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