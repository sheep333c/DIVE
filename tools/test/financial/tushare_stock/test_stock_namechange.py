"""
Tushare股票曾用名查询工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.financial.tushare_stock.stock_namechange import StockNameChangeTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestStockNameChangeTool(VerifiableToolTestBase):
    """Tushare股票曾用名查询工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "StockNameChangeTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            # 指定具体股票：平安银行（历史上有过改名）
            "ts_code": "000001.SZ",
            "start_date": "20000101",  # 更长的时间范围，确保能找到改名记录
            "end_date": "20241231",
            "fields": "ts_code,name,start_date,end_date,ann_date,change_reason"  # 获取完整字段信息
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return StockNameChangeTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx