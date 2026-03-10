"""
Bio.Restriction所有限制性内切酶列表工具
获取Bio.Restriction数据库中所有可用的限制性内切酶列表
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Restriction
from tools.core.tool import Tool


class RestrictionAllEnzymesTool(Tool):
    """所有限制性内切酶列表工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        获取所有可用的限制性内切酶列表
        
        参数:
        - limit: 返回的酶数量限制，默认100（总共1088个酶）
        - search_pattern: 搜索模式（可选），用于过滤酶名称
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                limit = params.get('limit', 100)
                search_pattern = params.get('search_pattern', '')
                
                # 获取所有酶
                all_enzymes = Restriction.AllEnzymes
                total_count = len(all_enzymes)
                
                # 转换为字符串列表
                enzyme_names = [str(enzyme) for enzyme in all_enzymes]
                
                # 如果有搜索模式，进行过滤
                if search_pattern:
                    enzyme_names = [name for name in enzyme_names 
                                   if search_pattern.lower() in name.lower()]
                
                # 应用限制
                limited_enzymes = enzyme_names[:limit]
                
                return {
                    'total_enzymes': total_count,
                    'filtered_count': len(enzyme_names) if search_pattern else total_count,
                    'returned_count': len(limited_enzymes),
                    'search_pattern': search_pattern if search_pattern else None,
                    'limit': limit,
                    'enzymes': limited_enzymes
                }
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"酶列表获取失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
