#!/usr/bin/env python3
"""Tests for EtfIndexTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_etf.etf_index import EtfIndexTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestEtfIndexTool(VerifiableToolTestBase):
    """Test suite for EtfIndexTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "EtfIndexTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "fields": "ts_code,indx_name,pub_date,bp"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return EtfIndexTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx