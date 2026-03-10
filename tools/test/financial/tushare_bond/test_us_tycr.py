#!/usr/bin/env python3
"""Tests for UsTycrTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.us_tycr import UsTycrTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestUsTycrTool(VerifiableToolTestBase):
    """Test suite for UsTycrTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "UsTycrTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "start_date": "20241101", "end_date": "20241201"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return UsTycrTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
