#!/usr/bin/env python3
"""Tests for OptBasicTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_options.opt_basic import OptBasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestOptBasicTool(VerifiableToolTestBase):
    """Test suite for OptBasicTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "OptBasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "exchange": "DCE",
            "fields": "ts_code,name,exercise_type,list_date,delist_date"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return OptBasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx