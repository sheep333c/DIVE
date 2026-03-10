#!/usr/bin/env python3
"""Tests for BcOtcqtTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.bc_otcqt import BcOtcqtTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBcOtcqtTool(VerifiableToolTestBase):
    """Test suite for BcOtcqtTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BcOtcqtTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "200013.BC", "start_date": "20241201", "end_date": "20241201"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return BcOtcqtTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
