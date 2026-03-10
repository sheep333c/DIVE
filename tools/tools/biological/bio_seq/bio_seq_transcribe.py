#!/usr/bin/env python3
"""
Bio.Seq Transcribe工具 - DNA转录和反转录

该工具使用BioPython的Bio.Seq转录功能。
"""

from typing import Dict, Any
from Bio.Seq import transcribe, back_transcribe
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqTranscribeTool(Tool):
    """
    Bio.Seq Transcribe工具
    
    使用BioPython的Bio.Seq转录功能提供DNA/RNA转录操作。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 获取参数
            sequence = params.get('sequence')
            operation = params.get('operation', 'transcribe')
            
            # 基本参数验证
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            
            # 清理序列
            clean_sequence = ''.join(sequence.upper().split())
            
            # 执行转录操作
            if operation == 'transcribe':
                result = str(transcribe(clean_sequence))
            elif operation == 'back_transcribe':
                result = str(back_transcribe(clean_sequence))
            else:
                return {"error": f"Invalid operation: {operation}"}
            
            return {"result": result}
            
        except Exception as e:
            return {"error": f"Transcription operation failed: {str(e)}"}
