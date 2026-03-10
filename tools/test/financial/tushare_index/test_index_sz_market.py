#!/usr/bin/env python3
"""Tests for IndexSzMarketTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_index.index_sz_market import IndexSzMarketTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIndexSzMarketTool(VerifiableToolTestBase):
    """Test suite for IndexSzMarketTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "IndexSzMarketTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "trade_date": "20241215",
            "fields": "trade_date,ts_count,amount"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IndexSzMarketTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx