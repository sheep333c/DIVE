#!/usr/bin/env python3
"""Tests for PublicFundDivTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_fund.fund_div import FundDivTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestFundDivTool(VerifiableToolTestBase):
    """Test suite for FundDivTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "FundDivTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "000001.OF",
            "fields": "ts_code,ann_date,imp_anndate,base_date,div_proc"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FundDivTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx