"""
Bio.Seq RNA互补工具
使用Bio.Seq.complement_rna获取RNA序列的互补序列
"""

import time
import os
import json
from typing import Dict, Any
from Bio.Seq import complement_rna
from tools.core.tool import Tool


class BioSeqComplementRnaTool(Tool):
    """RNA互补工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        获取RNA序列的互补序列
        
        参数:
        - sequence: RNA序列字符串
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                sequence = params.get('sequence', '')
                
                # 验证输入
                if not sequence:
                    return {"error": "序列参数是必需的"}
                
                # 获取RNA互补序列
                complement_seq = complement_rna(sequence)
                
                # 直接返回互补序列
                return str(complement_seq)
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"RNA互补失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
