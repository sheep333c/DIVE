#!/usr/bin/env python3
"""Tests for FutWsrTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_futures.fut_wsr import FutWsrTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFutWsrTool(VerifiableToolTestBase):
    """Test suite for FutWsrTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutWsrTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20231201",
            "symbol": "CU",
            "fields": "trade_date,symbol,name,warehouse,vol,vol_chg"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutWsrTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
