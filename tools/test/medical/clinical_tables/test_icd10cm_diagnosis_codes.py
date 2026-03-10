"""
ICD-10-CM诊断编码工具测试
基于VerifiableToolTestBase基类，简化透传设计
"""
from unittest.mock import MagicMock
from tools.medical.clinical_tables.icd10cm_diagnosis_codes import Icd10cmDiagnosisCodesTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestIcd10cmDiagnosisCodesTool(VerifiableToolTestBase):
    """ICD-10-CM诊断编码工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "Icd10cmDiagnosisCodesTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {
            "terms": "E11",              # 搜索Type 2 diabetes mellitus相关编码
            "count": 10,                 # 返回10个结果
            "offset": 0,                 # 从第0个开始
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return Icd10cmDiagnosisCodesTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx