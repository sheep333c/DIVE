#!/usr/bin/env python3
"""Tests for CbDailyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.cb_daily import CbDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCbDailyTool(VerifiableToolTestBase):
    """Test suite for CbDailyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CbDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20241201", "fields": "ts_code,trade_date,open,high,low,close"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CbDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
