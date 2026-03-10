#!/usr/bin/env python3
"""
测试股票停复牌工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_suspend import StockSuspendTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockSuspendTool(VerifiableToolTestBase):
    """股票停复牌工具测试类"""
    
    __test__ = True  
    TOOL_CLASS_NAME = "StockSuspendTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 查询2024年的停复牌信息
            "start_date": "20240101",
            "end_date": "20240331"  # 查询前3个月的数据，避免数据量过大
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockSuspendTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()