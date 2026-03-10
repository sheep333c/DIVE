#!/usr/bin/env python3
"""Tests for FutWeeklyDetailTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_futures.fut_weekly_detail import FutWeeklyDetailTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFutWeeklyDetailTool(VerifiableToolTestBase):
    """Test suite for FutWeeklyDetailTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutWeeklyDetailTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "week": "20231201",
            "prd": "IC",
            "fields": "week,prd,name,vol,vol_chg,amount,amount_chg"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutWeeklyDetailTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
