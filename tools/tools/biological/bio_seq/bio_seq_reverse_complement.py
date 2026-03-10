"""
Bio.Seq DNA反向互补工具
使用Bio.Seq.reverse_complement获取DNA序列的反向互补序列
"""

import time
import os
import json
from typing import Dict, Any
from Bio.Seq import reverse_complement
from tools.core.tool import Tool


class BioSeqReverseComplementTool(Tool):
    """DNA反向互补工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        获取DNA序列的反向互补序列
        
        参数:
        - sequence: DNA序列字符串
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
                
                # 获取反向互补序列
                rev_comp_seq = reverse_complement(sequence)
                
                # 直接返回反向互补序列
                return str(rev_comp_seq)
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"DNA反向互补失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
