#!/usr/bin/env python3
"""
测试股票资产负债表工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_balancesheet import StockBalanceSheetTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockBalanceSheetTool(VerifiableToolTestBase):
    """股票资产负债表工具测试类"""
    
    __test__ = True  
    TOOL_CLASS_NAME = "StockBalanceSheetTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "ts_code": "000001.SZ",
            "period": "20231231",
            "fields": "ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,total_assets,total_liab,total_hldr_eqy_exc_min_int"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockBalanceSheetTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()