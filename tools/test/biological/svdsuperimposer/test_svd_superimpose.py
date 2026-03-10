"""
测试Bio.SVDSuperimposer 3D结构叠合工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.svdsuperimposer.svd_superimpose import SvdSuperimposeTool


class TestSvdSuperimposeTool(VerifiableToolTestBase):
    """测试SvdSuperimposeTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "SvdSuperimposeTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'coordinates1': [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            'coordinates2': [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
            'include_transformed': False
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return SvdSuperimposeTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None