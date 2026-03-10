"""
测试Bio.Data.CodonTable根据ID获取遗传密码表工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.codon_table.codon_table_by_id import CodonTableByIdTool


class TestCodonTableByIdTool(VerifiableToolTestBase):
    """测试CodonTableByIdTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "CodonTableByIdTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'table_id': 2,  # 线粒体密码表
            'include_forward_table': False,
            'include_back_table': False
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return CodonTableByIdTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None