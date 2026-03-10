"""
OpenAlex文本分析工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.academic.openalex.openalex_analyze_text import OpenalexAnalyzeTextTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestOpenalexAnalyzeTextTool(VerifiableToolTestBase):
    """OpenAlex文本分析工具测试"""
    
    __test__ = True  # 确保pytest识别这个测试类
    TOOL_CLASS_NAME = "OpenalexAnalyzeTextTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "title": "Machine learning for diabetes research",
            "abstract": "This study explores applications of machine learning algorithms in diabetes mellitus research and patient care."
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return OpenalexAnalyzeTextTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx