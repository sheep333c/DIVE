#!/usr/bin/env python3
"""
测试股票基础列表工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_basic import StockBasicTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockBasicTool(VerifiableToolTestBase):
    """股票基础列表工具测试类"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "StockBasicTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 获取上交所的上市股票，限制数量避免返回过多数据
            "exchange": "SSE",
            "list_status": "L",
            "fields": "ts_code,symbol,name,area,industry,market,list_date"  # 获取主要字段
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockBasicTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()