"""
Bio.SeqFeature复合位置工具
创建复合序列特征位置（多个不连续片段）并提取序列
"""

import time
import os
import json
from typing import Dict, Any, List
from Bio import SeqFeature
from Bio.Seq import Seq
from tools.core.tool import Tool


class SeqFeatureCompoundTool(Tool):
    """复合序列特征位置工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        创建复合序列特征位置并提取多个片段
        
        参数:
        - sequence: 目标序列字符串
        - locations: 位置列表，每个位置包含start和end
        - extract: 是否提取序列片段，默认True
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                sequence = params.get('sequence', '')
                locations = params.get('locations', [])
                extract = params.get('extract', True)
                
                # 验证输入
                if not sequence:
                    return {"error": "序列参数是必需的"}
                if not locations:
                    return {"error": "位置列表是必需的"}
                
                # 创建FeatureLocation列表
                feature_locations = []
                for loc_data in locations:
                    start = loc_data.get('start')
                    end = loc_data.get('end')
                    strand = loc_data.get('strand')
                    
                    if start is None or end is None:
                        return {"error": f"位置数据缺少start或end: {loc_data}"}
                    
                    feature_locations.append(
                        SeqFeature.FeatureLocation(start, end, strand)
                    )
                
                # 创建CompoundLocation
                compound_location = SeqFeature.CompoundLocation(feature_locations)
                
                # 构建结果
                result = {
                    'part_count': len(compound_location.parts),
                    'total_length': len(compound_location),
                    'sequence_length': len(sequence),
                    'parts': []
                }
                
                # 添加各部分信息
                for i, part in enumerate(compound_location.parts):
                    part_info = {
                        'index': i,
                        'start': part.start,
                        'end': part.end,
                        'strand': part.strand,
                        'length': len(part)
                    }
                    result['parts'].append(part_info)
                
                # 可选提取序列片段
                if extract:
                    seq_obj = Seq(sequence)
                    extracted_seq = compound_location.extract(seq_obj)
                    result['extracted_sequence'] = str(extracted_seq)
                    result['extracted_length'] = len(extracted_seq)
                
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"复合序列特征位置处理失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
