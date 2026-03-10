#!/usr/bin/env python3
"""
Bio.Seq Translate工具 - DNA/RNA序列翻译

该工具使用BioPython的Bio.Seq.translate功能将核酸序列翻译为氨基酸序列。
"""

from typing import Dict, Any
from Bio.Seq import translate
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqTranslateTool(Tool):
    """
    Bio.Seq Translate工具
    
    使用BioPython的Bio.Seq.translate功能将核酸序列翻译为氨基酸序列。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 获取参数
            sequence = params.get('sequence')
            
            # 基本参数验证
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            
            # 清理序列
            clean_sequence = ''.join(sequence.upper().split())
            
            # 构建翻译参数
            translate_params = {'sequence': clean_sequence}
            
            # 添加可选参数
            if 'table' in params:
                translate_params['table'] = params['table']
            if 'stop_symbol' in params:
                translate_params['stop_symbol'] = params['stop_symbol']
            if 'to_stop' in params:
                translate_params['to_stop'] = params['to_stop']
            if 'cds' in params:
                translate_params['cds'] = params['cds']
            if 'gap' in params:
                translate_params['gap'] = params['gap']
            
            # 执行翻译
            protein_sequence = translate(**translate_params)
            
            return {"protein_sequence": str(protein_sequence)}
            
        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}
