"""
蛋白质序列全面分析工具
"""

import time
import json
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from Bio.SeqUtils.ProtParam import ProteinAnalysis


class ProtParamAnalysisTool(Tool):
    """蛋白质序列全面分析工具"""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """
        分析蛋白质序列的各种理化参数
        
        Args:
            context: 执行上下文
            params: 包含以下参数的字典
                - sequence: 蛋白质序列 (字符串)
        
        Returns:
            dict: 包含分子量、等电点、氨基酸组成等信息的字典
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
                    
                    # 收集所有分析结果
                    result = {
                        'molecular_weight': analysis.molecular_weight(),
                        'isoelectric_point': analysis.isoelectric_point(),
                        'aromaticity': analysis.aromaticity(),
                        'instability_index': analysis.instability_index(),
                        'gravy': analysis.gravy(),
                        'amino_acids_percent': analysis.amino_acids_percent,
                        'amino_acids_count': analysis.count_amino_acids(),
                        'length': analysis.length,
                        'secondary_structure_fraction': analysis.secondary_structure_fraction(),
                        'flexibility': analysis.flexibility(),
                        'molar_extinction_coefficient': analysis.molar_extinction_coefficient(),
                        'monoisotopic': analysis.monoisotopic
                    }
                    
                    return result
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(1 * (attempt + 1))
            return {"error": "Max retries exceeded"}
                    
        except Exception as e:
            return {"error": f"蛋白质分析失败: {str(e)}"}

    @classmethod
