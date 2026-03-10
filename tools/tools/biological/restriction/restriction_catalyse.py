"""
Bio.Restriction限制性内切酶切割工具
使用指定限制性内切酶切割DNA序列
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Restriction
from Bio.Seq import Seq
from tools.core.tool import Tool


class RestrictionCatalyseTool(Tool):
    """限制性内切酶切割工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        使用限制性内切酶切割DNA序列
        
        参数:
        - sequence: DNA序列字符串
        - enzyme_name: 限制性内切酶名称（如'EcoRI', 'BamHI'）
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                sequence = params.get('sequence', '')
                enzyme_name = params.get('enzyme_name', '')
                
                # 验证输入
                if not sequence:
                    return {"error": "序列参数是必需的"}
                if not enzyme_name:
                    return {"error": "酶名称参数是必需的"}
                
                # 获取限制性内切酶
                if not hasattr(Restriction, enzyme_name):
                    return {"error": f"未找到限制性内切酶: {enzyme_name}"}
                
                enzyme = getattr(Restriction, enzyme_name)
                
                # 创建序列对象并执行切割
                seq_obj = Seq(sequence)
                fragments = enzyme.catalyse(seq_obj)
                
                # 返回切割结果
                return {
                    'enzyme_name': enzyme_name,
                    'recognition_site': str(enzyme.site),
                    'original_sequence': sequence,
                    'fragments': [str(frag) for frag in fragments],
                    'fragment_count': len(fragments),
                    'fragment_lengths': [len(frag) for frag in fragments]
                }
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"限制性内切酶切割失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
