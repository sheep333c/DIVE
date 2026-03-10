#!/usr/bin/env python3
"""
测试股票财务指标工具
"""
import unittest
from unittest.mock import MagicMock

from tools.financial.tushare_stock.stock_fina_indicator import StockFinaIndicatorTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockFinaIndicatorTool(VerifiableToolTestBase):
    """股票财务指标工具测试类"""
    
    __test__ = True  
    TOOL_CLASS_NAME = "StockFinaIndicatorTool"
    
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
            # 选择核心财务指标字段
            "fields": "ts_code,ann_date,end_date,roe,roa,roe_waa,roe_dt,roa2_yearly,debt_to_assets,assets_to_eqt,dp_assets_to_eqt,ca_to_assets"
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockFinaIndicatorTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()