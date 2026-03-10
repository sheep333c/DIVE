#!/usr/bin/env python3
"""
测试股票分红送股工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_dividend import StockDividendTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockDividendTool(VerifiableToolTestBase):
    """股票分红送股工具测试类"""
    
    __test__ = True  
    TOOL_CLASS_NAME = "StockDividendTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 测试一个历史上有过分红的股票 - 平安银行
            "ts_code": "000001.SZ"
            # 不指定日期参数，获取该股票的所有历史分红记录
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockDividendTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()