#!/usr/bin/env python3
"""Tests for StockDcDailyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_dc_daily import StockDcDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockDcDailyTool(VerifiableToolTestBase):
    """Test suite for StockDcDailyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockDcDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {"trade_date": "20241201"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockDcDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()