#!/usr/bin/env python3
"""Tests for FxDailyTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_forex.fx_daily import FxDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFxDailyTool(VerifiableToolTestBase):
    """Test suite for FxDailyTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FxDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            'ts_code': 'USDCNH.FXCM',
            'start_date': '20240101',
            'end_date': '20240131',
            'exchange': 'FXCM'
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FxDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx