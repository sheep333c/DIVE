#!/usr/bin/env python3
"""Tests for IndexCiMemberTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_index.index_ci_member import IndexCiMemberTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIndexCiMemberTool(VerifiableToolTestBase):
    """Test suite for IndexCiMemberTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "IndexCiMemberTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "index_code": "CI005001.CI",
            "fields": "index_code,con_code,in_date,out_date"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IndexCiMemberTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx