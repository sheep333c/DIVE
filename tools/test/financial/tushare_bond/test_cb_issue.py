#!/usr/bin/env python3
"""Tests for CbIssueTool."""

from unittest.mock import MagicMock
from tools.financial.tushare_bond.cb_issue import CbIssueTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestCbIssueTool(VerifiableToolTestBase):
    """Test suite for CbIssueTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "CbIssueTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """Return test parameters for the tool."""
        return {
            "ann_date": "20241201", "fields": "ts_code,ann_date,issue_size"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CbIssueTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
