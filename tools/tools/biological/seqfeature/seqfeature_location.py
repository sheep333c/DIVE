"""
Bio.SeqFeature位置创建和序列提取工具
创建序列特征位置并从序列中提取指定片段
"""

import time
import os
import json
from typing import Dict, Any
from Bio import SeqFeature
from Bio.Seq import Seq
from tools.core.tool import Tool


class SeqFeatureLocationTool(Tool):
    """序列特征位置工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        创建序列特征位置并提取序列片段
        
        参数:
        - sequence: 目标序列字符串
        - start: 起始位置（0-based）
        - end: 结束位置（0-based，不包含）
        - strand: 链方向（1=正链, -1=负链, None=未指定），默认None
        - extract: 是否提取序列片段，默认True
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                sequence = params.get('sequence', '')
                start = params.get('start')
                end = params.get('end')
                strand = params.get('strand')
                extract = params.get('extract', True)
                
                # 验证输入
                if not sequence:
                    return {"error": "序列参数是必需的"}
                if start is None:
                    return {"error": "起始位置是必需的"}
                if end is None:
                    return {"error": "结束位置是必需的"}
                
                # 创建FeatureLocation
                location = SeqFeature.FeatureLocation(start, end, strand)
                
                # 构建结果
                result = {
                    'start': location.start,
                    'end': location.end,
                    'strand': location.strand,
                    'length': len(location),
                    'sequence_length': len(sequence)
                }
                
                # 可选提取序列片段
                if extract:
                    seq_obj = Seq(sequence)
                    extracted_seq = location.extract(seq_obj)
                    result['extracted_sequence'] = str(extracted_seq)
                    result['extracted_length'] = len(extracted_seq)
                
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"序列特征位置处理失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
