"""
蛋白质分子量计算工具
"""

import time
import json
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from Bio.SeqUtils.ProtParam import ProteinAnalysis


class ProtParamMolecularWeightTool(Tool):
    """蛋白质分子量计算工具"""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """
        计算蛋白质序列的分子量
        
        Args:
            context: 执行上下文
            params: 包含以下参数的字典
                - sequence: 蛋白质序列 (字符串)
        
        Returns:
            float: 蛋白质分子量 (Da)
        """
        try:
            sequence = params.get('sequence')
            
            if not sequence:
                return {"error": "缺少必需参数: sequence"}
            
            # 实现重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    analysis = ProteinAnalysis(sequence)
                    return analysis.molecular_weight()
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(1 * (attempt + 1))
            return {"error": "Max retries exceeded"}
                    
        except Exception as e:
            return {"error": f"分子量计算失败: {str(e)}"}

    @classmethod
