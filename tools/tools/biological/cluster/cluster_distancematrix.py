"""
Bio.Cluster距离矩阵计算工具
使用Bio.Cluster.distancematrix计算数据点之间的距离矩阵
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Cluster
from tools.core.tool import Tool


class ClusterDistancematrixTool(Tool):
    """距离矩阵计算工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        计算数据点之间的距离矩阵
        
        参数:
        - data: 数据矩阵（二维列表）
        - dist: 距离度量，默认'e'（欧几里得距离）
        - transpose: 是否转置数据，默认False
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                data = params.get('data')
                dist = params.get('dist', 'e')
                transpose = params.get('transpose', False)
                
                # 计算距离矩阵
                distance_matrix = Cluster.distancematrix(
                    data=data,
                    dist=dist,
                    transpose=transpose
                )
                
                # 将距离矩阵转换为列表格式返回
                if hasattr(distance_matrix, 'tolist'):
                    return distance_matrix.tolist()
                else:
                    # 如果是list of arrays，转换每个array
                    return [row.tolist() if hasattr(row, 'tolist') else list(row) 
                           for row in distance_matrix]
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"Distance matrix calculation failed: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
