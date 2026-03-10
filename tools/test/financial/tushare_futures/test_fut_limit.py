import pytest
from tools.financial.tushare_futures.fut_limit import FutLimitTool
from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.core.types import ExecutionContext


class TestFutLimitTool(VerifiableToolTestBase):
    """测试期货合约涨跌停价格工具"""
    
    __test__ = True
    TOOL_CLASS_NAME = "FutLimitTool"
    
    def get_tool_instance(self):
        """返回工具实例"""
        return FutLimitTool()
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            "trade_date": "20231201",
            "fields": "ts_code,symbol,trade_date,up_limit,down_limit"
        }
    
    def get_execution_context(self):
        """返回执行上下文"""
        from unittest.mock import MagicMock
        mock_ctx = MagicMock(spec=ExecutionContext)
        mock_ctx.timeout_ms = 30000
        return mock_ctx