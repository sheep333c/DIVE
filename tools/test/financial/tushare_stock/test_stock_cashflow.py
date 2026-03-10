#!/usr/bin/env python3
"""
测试股票现金流量表工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_cashflow import StockCashFlowTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockCashFlowTool(VerifiableToolTestBase):
    """股票现金流量表工具测试类"""
    
    __test__ = True  
    TOOL_CLASS_NAME = "StockCashFlowTool"
    
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
            "fields": "ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,n_cashflow_act,n_cashflow_inv_act,n_cashflow_fin_act"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockCashFlowTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()