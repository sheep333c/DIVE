"""
RxnormGetMultiIngredBrand工具测试
基于新的VerifiableToolTestBase基类，专注于工具特定的配置和实现
"""
from unittest.mock import MagicMock
from tools.medical.rxnav.rxnorm_get_multi_ingred_brand import RxnormGetMultiIngredBrandTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestRxnormGetMultiIngredBrandTool(VerifiableToolTestBase):
    """获取Rxnorm多成分品牌的工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RxnormGetMultiIngredBrandTool"
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.tool = RxnormGetMultiIngredBrandTool()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        """返回用于真实API调用的测试参数"""
        return {"ingredientids": "161+1191"}  # 使用正确的全小写参数名
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RxnormGetMultiIngredBrandTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return self.mock_ctx
    
    def get_urlopen_patch_path(self):
        """返回RxNAV工具的urlopen patch路径"""
        return 'tools.medical.rxnav.rxnorm_get_multi_ingred_brand.urlopen'
    
    def validate_error_response(self, result):
        """验证RxNAV工具的错误响应格式"""
        self.assertIn("error", result, "RxNAV tool error response should contain 'error' field")
        self.assertIsInstance(result["error"], str, "Error message should be a string")
    
    def get_mock_response_data(self):
        """返回Rxnorm API原始响应格式"""
        return {"brandGroup": {"conceptProperties": [{"rxcui": "123456", "name": "Tylenol PM", "tty": "BN"}]}}
    
    def get_expected_response_keys(self):
        """返回预期的响应键列表"""
        return ["success", "data", "brands"]
    
    def get_required_param_name(self):
        """返回必需参数名称"""
        return "ingredientids"