#!/usr/bin/env python3
"""Tests for IndexSwDailyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_index.index_sw_daily import IndexSwDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIndexSwDailyTool(VerifiableToolTestBase):
    """Test suite for IndexSwDailyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "IndexSwDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "801010.SI",
            "start_date": "20241201",
            "end_date": "20241215"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IndexSwDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx