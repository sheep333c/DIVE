#!/usr/bin/env python3
"""Tests for StockMarginDetailTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_margin_detail import StockMarginDetailTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockMarginDetailTool(VerifiableToolTestBase):
    """Test suite for StockMarginDetailTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockMarginDetailTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20240315"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockMarginDetailTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx