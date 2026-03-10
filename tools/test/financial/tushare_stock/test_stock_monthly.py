#!/usr/bin/env python3
"""Tests for StockMonthlyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_monthly import StockMonthlyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockMonthlyTool(VerifiableToolTestBase):
    """Test suite for StockMonthlyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockMonthlyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "000001.SZ",
            "start_date": "20240101",
            "end_date": "20240331"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockMonthlyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx