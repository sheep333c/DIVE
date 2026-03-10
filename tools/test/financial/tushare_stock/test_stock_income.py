#!/usr/bin/env python3
"""
测试股票利润表工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_income import StockIncomeTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockIncomeTool(VerifiableToolTestBase):
    """股票利润表工具测试类"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "StockIncomeTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 获取平安银行最近的利润表数据
            "ts_code": "000001.SZ",
            "period": "20231231",  # 2023年年报
            # 可以添加fields参数来限制返回的字段，提高性能
            "fields": "ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps,total_revenue,revenue,n_income,n_income_attr_p"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockIncomeTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()