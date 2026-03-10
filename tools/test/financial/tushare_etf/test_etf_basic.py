#!/usr/bin/env python3
"""Tests for EtfBasicTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_etf.etf_basic import EtfBasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestEtfBasicTool(VerifiableToolTestBase):
    """Test suite for EtfBasicTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "EtfBasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "list_status": "L",
            "fields": "ts_code,name,mgr_name,exchange"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return EtfBasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx