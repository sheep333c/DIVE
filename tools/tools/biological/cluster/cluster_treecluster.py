"""
Bio.Cluster层次聚类工具
使用Bio.Cluster.treecluster进行层次聚类分析
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Cluster
from tools.core.tool import Tool


class ClusterTreeclusterTool(Tool):
    """层次聚类工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        执行层次聚类分析
        
        参数:
        - data: 数据矩阵（二维列表）
        - method: 聚类方法，默认'm'（最大距离）
        - dist: 距离度量，默认'e'（欧几里得距离）
        - transpose: 是否转置数据，默认False
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                data = params.get('data')
                method = params.get('method', 'm')
                dist = params.get('dist', 'e')
                transpose = params.get('transpose', False)
                
                # 执行层次聚类
                tree = Cluster.treecluster(
                    data=data,
                    method=method,
                    dist=dist,
                    transpose=transpose
                )
                
                # 将Tree对象转换为可序列化的格式
                # Tree对象是可索引的，每个节点有left, right, distance属性
                tree_data = []
                for i in range(len(tree)):
                    node = tree[i]
                    tree_data.append({
                        'left': node.left,
                        'right': node.right, 
                        'distance': node.distance
                    })
                
                return tree_data
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"Hierarchical clustering failed: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
