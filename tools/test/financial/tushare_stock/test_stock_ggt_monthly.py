#!/usr/bin/env python3
"""Tests for StockGgtMonthlyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_ggt_monthly import StockGgtMonthlyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockGgtMonthlyTool(VerifiableToolTestBase):
    """Test suite for StockGgtMonthlyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockGgtMonthlyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {"month": "202411"}
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockGgtMonthlyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()