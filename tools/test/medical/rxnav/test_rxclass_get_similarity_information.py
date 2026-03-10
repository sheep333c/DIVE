"""
RxclassGetSimilarityInformation工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxclass_get_similarity_information import RxclassGetSimilarityInformationTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxclassGetSimilarityInformationTool(VerifiableToolTestBase):
    """获取Rxclass相似性信息的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxclassGetSimilarityInformationTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        # 使用API文档中的有效示例参数
        return {
            "classId1": "N02AA",           # ATC "natural opium alkaloids"
            "relaSource1": "ATC",          # ATC关系来源
            "rela1": "",                   # ATC类关系（可以为空）
            "classId2": "N0000175684",     # MoA "Full Opioid Agonists" 
            "relaSource2": "dailymed",     # DailyMed关系来源
            "rela2": "has_moa"             # 作用机制关系
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxclassGetSimilarityInformationTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    
