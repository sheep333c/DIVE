#!/usr/bin/env python3
"""Tests for CnMTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_macro.cn_m import CnMTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCnMTool(VerifiableToolTestBase):
    """Test suite for CnMTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CnMTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "start_m": "202301", "end_m": "202312"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CnMTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
