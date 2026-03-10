"""
测试Bio.Restriction限制性内切酶搜索工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.restriction.restriction_search import RestrictionSearchTool


class TestRestrictionSearchTool(VerifiableToolTestBase):
    """测试RestrictionSearchTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RestrictionSearchTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'sequence': 'GAATTCATGAATTC',
            'enzyme_name': 'EcoRI'
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RestrictionSearchTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None