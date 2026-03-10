"""
测试Bio.SeqFeature复合位置工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.seqfeature.seqfeature_compound import SeqFeatureCompoundTool


class TestSeqFeatureCompoundTool(VerifiableToolTestBase):
    """测试SeqFeatureCompoundTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "SeqFeatureCompoundTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'sequence': 'ATCGATCGATCGATCG',
            'locations': [
                {'start': 2, 'end': 6},
                {'start': 10, 'end': 14}
            ],
            'extract': True
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return SeqFeatureCompoundTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None