"""
ArXiv按ID获取论文工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.academic.arxiv.arxiv_get_papers_by_ids import ArxivGetPapersByIdsTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestArxivGetPapersByIdsTool(VerifiableToolTestBase):
    """ArXiv按ID获取论文工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "ArxivGetPapersByIdsTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "id_list": "1706.03762,1708.07747"  # Attention Is All You Need, Transformer papers
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return ArxivGetPapersByIdsTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    
    def get_expected_response_keys(self):
        """返回预期的响应键列表"""
        return ["success", "data"]
    