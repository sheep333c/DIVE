"""
Bio.Seq RNA反转录工具
使用Bio.Seq.back_transcribe将RNA序列转换为DNA序列
"""

import time
import os
import json
from typing import Dict, Any
from Bio.Seq import back_transcribe
from tools.core.tool import Tool


class BioSeqBackTranscribeTool(Tool):
    """RNA反转录工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        将RNA序列反转录为DNA序列
        
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
                
                # 执行反转录
                dna_sequence = back_transcribe(sequence)
                
                # 直接返回DNA序列
                return str(dna_sequence)
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"RNA反转录失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
