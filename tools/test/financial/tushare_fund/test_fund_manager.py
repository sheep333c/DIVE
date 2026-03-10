#!/usr/bin/env python3
"""Tests for PublicFundManagerTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_fund.fund_manager import FundManagerTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFundManagerTool(VerifiableToolTestBase):
    """Test suite for FundManagerTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FundManagerTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "000001.OF",
            "fields": "ts_code,ann_date,name,gender"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FundManagerTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx