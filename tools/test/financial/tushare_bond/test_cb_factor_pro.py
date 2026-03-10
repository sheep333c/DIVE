#!/usr/bin/env python3
"""Tests for CbFactorProTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.cb_factor_pro import CbFactorProTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCbFactorProTool(VerifiableToolTestBase):
    """Test suite for CbFactorProTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CbFactorProTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "113632.SH"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CbFactorProTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
