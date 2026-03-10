#!/usr/bin/env python3
"""Tests for CbCallTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.cb_call import CbCallTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCbCallTool(VerifiableToolTestBase):
    """Test suite for CbCallTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CbCallTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "fields": "ts_code,call_type,is_call,ann_date,call_date,call_price"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CbCallTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
