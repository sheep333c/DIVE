#!/usr/bin/env python3
"""Tests for StockGgtTop10Tool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_ggt_top10 import StockGgtTop10Tool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockGgtTop10Tool(VerifiableToolTestBase):
    """Test suite for StockGgtTop10Tool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockGgtTop10Tool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20240315",
            "market_type": "1"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockGgtTop10Tool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx