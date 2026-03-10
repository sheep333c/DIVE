#!/usr/bin/env python3
"""
Bio.Seq Complement工具 - 序列互补和反向互补

该工具使用BioPython的Bio.Seq互补功能。
"""

from typing import Dict, Any
from Bio.Seq import complement, reverse_complement, complement_rna, reverse_complement_rna
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqComplementTool(Tool):
    """
    Bio.Seq Complement工具
    
    使用BioPython的Bio.Seq互补功能提供序列互补操作。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 获取参数
            sequence = params.get('sequence')
            operation = params.get('operation', 'reverse_complement')
            
            # 基本参数验证
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            
            # 清理序列
            clean_sequence = ''.join(sequence.upper().split())
            
            # 执行互补操作
            if operation == 'complement':
                result = str(complement(clean_sequence))
            elif operation == 'reverse_complement':
                result = str(reverse_complement(clean_sequence))
            elif operation == 'complement_rna':
                result = str(complement_rna(clean_sequence))
            elif operation == 'reverse_complement_rna':
                result = str(reverse_complement_rna(clean_sequence))
            else:
                return {"error": f"Invalid operation: {operation}"}
            
            return {"result": result}
            
        except Exception as e:
            return {"error": f"Complement operation failed: {str(e)}"}
