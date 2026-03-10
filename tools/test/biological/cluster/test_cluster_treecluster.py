"""
测试Bio.Cluster层次聚类工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.cluster.cluster_treecluster import ClusterTreeclusterTool


class TestClusterTreeclusterTool(VerifiableToolTestBase):
    """测试ClusterTreeclusterTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "ClusterTreeclusterTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'data': [[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]]
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return ClusterTreeclusterTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return None