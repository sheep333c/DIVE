"""
Bio.Restriction限制性内切酶信息查询工具
获取指定限制性内切酶的详细信息
"""

import time
import os
import json
from typing import Dict, Any
from Bio import Restriction
from tools.core.tool import Tool


class RestrictionEnzymeInfoTool(Tool):
    """限制性内切酶信息查询工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        获取限制性内切酶的详细信息
        
        参数:
        - enzyme_name: 限制性内切酶名称（如'EcoRI', 'BamHI'）
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                enzyme_name = params.get('enzyme_name', '')
                
                # 验证输入
                if not enzyme_name:
                    return {"error": "酶名称参数是必需的"}
                
                # 获取限制性内切酶
                if not hasattr(Restriction, enzyme_name):
                    return {"error": f"未找到限制性内切酶: {enzyme_name}"}
                
                enzyme = getattr(Restriction, enzyme_name)
                
                # 收集酶信息
                enzyme_info = {
                    'name': enzyme_name,
                    'recognition_site': str(enzyme.site),
                    'site_length': len(enzyme.site)
                }
                
                # 获取可选信息
                try:
                    enzyme_info['suppliers'] = enzyme.all_suppliers()
                except:
                    enzyme_info['suppliers'] = []
                
                try:
                    enzyme_info['buffers'] = enzyme.buffers()
                except:
                    enzyme_info['buffers'] = []
                
                try:
                    enzyme_info['compatible_ends'] = [str(end) for end in enzyme.compatible_end()]
                except:
                    enzyme_info['compatible_ends'] = []
                
                try:
                    enzyme_info['characteristics'] = enzyme.characteristic()
                except:
                    enzyme_info['characteristics'] = []
                
                return enzyme_info
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"酶信息查询失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
