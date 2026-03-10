#!/usr/bin/env python3
"""Tests for FutBasicTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_futures.fut_basic import FutBasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFutBasicTool(VerifiableToolTestBase):
    """Test suite for FutBasicTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutBasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "exchange": "CFFEX",
            "fields": "ts_code,symbol,name,fut_code,multiplier,trade_unit"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutBasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
