"""
上市公司公告工具测试
"""
import unittest
from unittest.mock import MagicMock
from tools.financial.tushare_llm.anns_d import AnnsDTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestAnnsDTool(VerifiableToolTestBase):
    """上市公司公告工具测试类"""
    __test__ = True
    TOOL_CLASS_NAME = "AnnsDTool"
    
    def get_tool_instance(self):
        """获取工具实例"""
        return AnnsDTool()
    
    def get_test_params(self):
        """获取测试参数"""
        return {
            'ann_date': '20240601',  # 使用更近期的日期
            'ts_code': '000001.SZ'   # 限定特定股票减少数据量
        }
    
    def setUp(self):
        """测试设置"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
        self.tool = self.get_tool_instance()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()