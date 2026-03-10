"""
Bio.Cluster主成分分析工具
使用Bio.Cluster.pca进行主成分分析
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Cluster
from tools.core.tool import Tool


class ClusterPcaTool(Tool):
    """主成分分析工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        执行主成分分析
        
        参数:
        - data: 数据矩阵（二维列表）
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                data = params.get('data')
                
                # 执行PCA分析
                columnmean, coordinates, components, eigenvalues = Cluster.pca(data)
                
                # 直接返回PCA结果
                return {
                    'columnmean': columnmean.tolist() if hasattr(columnmean, 'tolist') else list(columnmean),
                    'coordinates': coordinates.tolist() if hasattr(coordinates, 'tolist') else [row.tolist() if hasattr(row, 'tolist') else list(row) for row in coordinates],
                    'components': components.tolist() if hasattr(components, 'tolist') else [row.tolist() if hasattr(row, 'tolist') else list(row) for row in components],
                    'eigenvalues': eigenvalues.tolist() if hasattr(eigenvalues, 'tolist') else list(eigenvalues)
                }
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"PCA analysis failed: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
