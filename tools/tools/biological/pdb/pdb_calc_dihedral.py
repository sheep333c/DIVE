"""
PDB二面角计算工具。

此工具计算四个3D点构成的二面角。
"""

from typing import Dict, Any, List
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PdbCalcDihedralTool(Tool):
    """
    PDB二面角计算工具。
    
    使用Bio.PDB计算四个3D点构成的二面角，
    返回以弧度为单位的二面角值。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算四点二面角。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - v1 (List[float]): 第一个点的坐标 [x, y, z]
                - v2 (List[float]): 第二个点的坐标 [x, y, z]
                - v3 (List[float]): 第三个点的坐标 [x, y, z]
                - v4 (List[float]): 第四个点的坐标 [x, y, z]
        
        Returns:
            二面角值(弧度)
        """
        try:
            from Bio.PDB import calc_dihedral
            from Bio.PDB.vectors import Vector
            
            # 提取参数
            v1 = params.get('v1', [])
            v2 = params.get('v2', [])
            v3 = params.get('v3', [])
            v4 = params.get('v4', [])
            
            # 验证输入
            for i, v in enumerate([v1, v2, v3, v4], 1):
                if not isinstance(v, list) or len(v) != 3:
                    return {"error": f"v{i}必须是包含3个数值的列表"}
                for coord in v:
                    if not isinstance(coord, (int, float)):
                        return {"error": f"v{i}的坐标必须是数值"}
            
            # 执行带重试机制的计算
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 创建Vector对象
                    vec1 = Vector(*v1)
                    vec2 = Vector(*v2)
                    vec3 = Vector(*v3)
                    vec4 = Vector(*v4)
                    
                    # 计算二面角
                    dihedral = calc_dihedral(vec1, vec2, vec3, vec4)
                    
                    # 直接返回二面角值(弧度)
                    return float(dihedral)
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            return {"error": str(e)}
