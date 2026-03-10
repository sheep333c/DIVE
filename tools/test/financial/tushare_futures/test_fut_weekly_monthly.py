#!/usr/bin/env python3
"""Tests for FutWeeklyMonthlyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_futures.fut_weekly_monthly import FutWeeklyMonthlyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFutWeeklyMonthlyTool(VerifiableToolTestBase):
    """Test suite for FutWeeklyMonthlyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutWeeklyMonthlyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "start_date": "20240101",  # 开始日期
            "end_date": "20240331",    # 结束日期
            "freq": "week"            # 必需参数：周线数据
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutWeeklyMonthlyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
