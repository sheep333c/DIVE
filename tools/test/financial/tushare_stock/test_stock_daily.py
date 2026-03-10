#!/usr/bin/env python3
"""
测试股票日线行情工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_daily import StockDailyTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockDailyTool(VerifiableToolTestBase):
    """股票日线行情工具测试类"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "StockDailyTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 获取平安银行最近3天的行情数据
            "ts_code": "000001.SZ",
            "start_date": "20240301",
            "end_date": "20240305"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockDailyTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()