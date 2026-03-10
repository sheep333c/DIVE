"""
Bio.SVDSuperimposer 3D结构叠合工具
使用SVD算法进行两组3D坐标的最优叠合分析
"""

import time
import os
import json
import numpy as np
from typing import Dict, Any
from Bio import SVDSuperimposer
from tools.core.tool import Tool


class SvdSuperimposeTool(Tool):
    """3D结构叠合工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        执行3D结构叠合分析
        
        参数:
        - coordinates1: 第一组3D坐标（参考结构）
        - coordinates2: 第二组3D坐标（待叠合结构）
        - include_transformed: 是否包含变换后的坐标，默认False
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                coord1 = params.get('coordinates1')
                coord2 = params.get('coordinates2')
                include_transformed = params.get('include_transformed', False)
                
                # 验证输入
                if coord1 is None:
                    return {"error": "第一组坐标是必需的"}
                if coord2 is None:
                    return {"error": "第二组坐标是必需的"}
                
                # 转换为numpy数组
                coord1_array = np.array(coord1)
                coord2_array = np.array(coord2)
                
                # 验证坐标形状
                if coord1_array.shape != coord2_array.shape:
                    return {"error": f"坐标形状不匹配: {coord1_array.shape} vs {coord2_array.shape}"}
                
                if len(coord1_array.shape) != 2 or coord1_array.shape[1] != 3:
                    return {"error": f"坐标必须是Nx3的数组，实际形状: {coord1_array.shape}"}
                
                # 创建SVDSuperimposer实例
                sup = SVDSuperimposer.SVDSuperimposer()
                
                # 设置坐标
                sup.set(coord1_array, coord2_array)
                
                # 计算初始RMS
                initial_rms = sup.get_init_rms()
                
                # 运行叠合计算
                sup.run()
                
                # 获取结果
                final_rms = sup.get_rms()
                rot_matrix, translation = sup.get_rotran()
                
                # 构建结果
                result = {
                    'initial_rms': float(initial_rms),
                    'final_rms': float(final_rms),
                    'rotation_matrix': rot_matrix.tolist(),
                    'translation_vector': translation.tolist(),
                    'coordinate_count': len(coord1_array),
                    'improvement': float(initial_rms - final_rms)
                }
                
                # 可选包含变换后的坐标
                if include_transformed:
                    transformed_coords = sup.get_transformed()
                    result['transformed_coordinates'] = transformed_coords.tolist()
                
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"3D结构叠合失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
