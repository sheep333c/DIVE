#!/usr/bin/env python3
"""Tests for IndexSwMemberTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_index.index_sw_member import IndexSwMemberTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIndexSwMemberTool(VerifiableToolTestBase):
    """Test suite for IndexSwMemberTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "IndexSwMemberTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "index_code": "801010.SI",
            "fields": "index_code,con_code,in_date,out_date"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IndexSwMemberTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx