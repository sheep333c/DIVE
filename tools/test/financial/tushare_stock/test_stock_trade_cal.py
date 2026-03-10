#!/usr/bin/env python3
"""Tests for StockTradeCal."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_trade_cal import StockTradeCalTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockTradeCal(VerifiableToolTestBase):
    """Test suite for StockTradeCal."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockTradeCalTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "exchange": "SSE",
            "start_date": "20240301",
            "end_date": "20240331"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockTradeCalTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx