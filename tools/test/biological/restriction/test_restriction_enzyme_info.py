"""
测试Bio.Restriction限制性内切酶信息查询工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.restriction.restriction_enzyme_info import RestrictionEnzymeInfoTool


class TestRestrictionEnzymeInfoTool(VerifiableToolTestBase):
    """测试RestrictionEnzymeInfoTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "RestrictionEnzymeInfoTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'enzyme_name': 'BamHI'
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return RestrictionEnzymeInfoTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None