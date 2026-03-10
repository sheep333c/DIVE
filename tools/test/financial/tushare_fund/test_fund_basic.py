#!/usr/bin/env python3
"""Tests for PublicFundBasicTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_fund.fund_basic import FundBasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFundBasicTool(VerifiableToolTestBase):
    """Test suite for FundBasicTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FundBasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "status": "L",
            "fields": "ts_code,name,management,custodian,fund_type"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FundBasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx