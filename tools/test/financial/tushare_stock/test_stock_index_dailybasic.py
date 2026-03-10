#!/usr/bin/env python3
"""Tests for StockIndexDailybasicTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_index_dailybasic import StockIndexDailybasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockIndexDailybasicTool(VerifiableToolTestBase):
    """Test suite for StockIndexDailybasicTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockIndexDailybasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "000001.SH",
            "start_date": "20240301",
            "end_date": "20240315"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockIndexDailybasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx