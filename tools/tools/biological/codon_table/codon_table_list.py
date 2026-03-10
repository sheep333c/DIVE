"""
Bio.Data.CodonTable所有遗传密码表列表工具
列出所有可用的遗传密码表及其基本信息
"""

import time
import os
import json
from typing import Dict, Any
from Bio.Data import CodonTable
from tools.core.tool import Tool


class CodonTableListTool(Tool):
    """所有遗传密码表列表工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        列出所有可用的遗传密码表
        
        参数:
        - include_details: 是否包含详细信息（起始/终止密码子），默认True
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                include_details = params.get('include_details', True)
                
                # 获取所有遗传密码表
                all_tables = CodonTable.ambiguous_dna_by_id
                
                # 构建结果
                result = {
                    'total_tables': len(all_tables),
                    'available_ids': sorted(list(all_tables.keys())),
                    'tables': []
                }
                
                # 遍历所有密码表
                for table_id in sorted(all_tables.keys()):
                    table = all_tables[table_id]
                    
                    table_info = {
                        'id': table.id,
                        'names': list(table.names),
                        'primary_name': table.names[0] if table.names else f"Table {table_id}"
                    }
                    
                    # 可选包含详细信息
                    if include_details:
                        table_info.update({
                            'start_codons_count': len(table.start_codons),
                            'stop_codons_count': len(table.stop_codons),
                            'start_codons': list(table.start_codons),
                            'stop_codons': list(table.stop_codons)
                        })
                    
                    result['tables'].append(table_info)
                
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"获取遗传密码表列表失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
