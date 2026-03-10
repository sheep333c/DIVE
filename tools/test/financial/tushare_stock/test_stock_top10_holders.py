#!/usr/bin/env python3
"""Tests for StockTop10HoldersTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_top10_holders import StockTop10HoldersTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockTop10HoldersTool(VerifiableToolTestBase):
    """Test suite for StockTop10HoldersTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "StockTop10HoldersTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ts_code": "000001.SZ",
            "period": "20231231"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockTop10HoldersTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx