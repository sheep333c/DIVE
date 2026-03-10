#!/usr/bin/env python3
"""Tests for IndexDailyInfoTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_index.index_daily_info import IndexDailyInfoTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIndexDailyInfoTool(VerifiableToolTestBase):
    """Test suite for IndexDailyInfoTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "IndexDailyInfoTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20241215",
            "fields": "ts_code,trade_date,turnover_rate,pe"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IndexDailyInfoTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx