#!/usr/bin/env python3
"""Tests for FutDailyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_futures.fut_daily import FutDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFutDailyTool(VerifiableToolTestBase):
    """Test suite for FutDailyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20231201",
            "exchange": "CFFEX",
            "fields": "ts_code,trade_date,open,high,low,close,vol,amount"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
