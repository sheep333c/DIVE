#!/usr/bin/env python3
"""Tests for CnGdpTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_macro.cn_gdp import CnGdpTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCnGdpTool(VerifiableToolTestBase):
    """Test suite for CnGdpTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CnGdpTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "start_q": "2023Q1", "end_q": "2024Q1"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CnGdpTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
