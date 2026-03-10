#!/usr/bin/env python3
"""Tests for CbShareTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.cb_share import CbShareTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCbShareTool(VerifiableToolTestBase):
    """Test suite for CbShareTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CbShareTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "113001.SH", "fields": "ts_code,end_date,convert_price"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CbShareTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
