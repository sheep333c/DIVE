#!/usr/bin/env python3
"""Tests for CnPmiTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_macro.cn_pmi import CnPmiTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCnPmiTool(VerifiableToolTestBase):
    """Test suite for CnPmiTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CnPmiTool"
    
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
        return CnPmiTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
