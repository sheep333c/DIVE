"""
测试Bio.Data.IUPACData字母表查询工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.iupac_data.iupac_data_letters import IupacDataLettersTool


class TestIupacDataLettersTool(VerifiableToolTestBase):
    """测试IupacDataLettersTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "IupacDataLettersTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'sequence_type': 'dna',
            'include_ambiguous': True
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return IupacDataLettersTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None