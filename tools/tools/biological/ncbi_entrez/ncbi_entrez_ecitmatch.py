#!/usr/bin/env python3
"""
NCBI Entrez ECitMatch工具 - 文献引用匹配

该工具使用BioPython的Bio.Entrez.ecitmatch功能根据引用字符串检索PMID，
用于文献引用的自动匹配和验证。
"""

import os
import time
from typing import Dict, Any
from Bio import Entrez
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class NcbiEntrezEcitmatchTool(Tool):
    """
    NCBI Entrez ECitMatch工具
    
    使用BioPython的Bio.Entrez.ecitmatch功能根据引用字符串检索PMID。
    
    主要功能：
    - 根据期刊名、卷号、页码等信息匹配PMID
    - 支持批量引用匹配
    - 用于文献管理和引用验证
    """
    
    def _setup_entrez(self):
        """设置Entrez配置"""
        config_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ncbi_key.txt')
        api_key = None
        email = None
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('api_key='):
                            api_key = line.split('=', 1)[1]
                        elif line.startswith('email='):
                            email = line.split('=', 1)[1]
            except Exception:
                pass

        # Fallback to environment variables
        api_key = api_key or os.getenv("NCBI_API_KEY", "")
        email = email or os.getenv("NCBI_EMAIL", "")

        if not hasattr(Entrez, 'email') or not Entrez.email:
            Entrez.email = email if email else "user@example.org"
        
        if api_key and (not hasattr(Entrez, 'api_key') or not Entrez.api_key):
            Entrez.api_key = api_key
    
    def _validate_citation_string(self, citation: str) -> bool:
        """验证引用字符串格式"""
        if not citation or not isinstance(citation, str):
            return False
        
        # 引用字符串应该包含期刊名、年份、卷号、页码等信息
        # 格式通常为: journal_title|year|volume|first_page|author_name|your_key|
        parts = citation.split('|')
        if len(parts) < 4:  # 至少需要期刊、年份、卷号、页码
            return False
        
        # 检查年份是否为数字
        try:
            year = parts[1].strip()
            if year and not year.isdigit():
                return False
        except:
            return False
        
        return True
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self._setup_entrez()
            
            # 获取参数
            bdata = params.get('bdata')
            
            # 参数验证
            if not bdata:
                return {"error": "Missing required parameter: bdata"}
            
            if not isinstance(bdata, str) or len(bdata.strip()) == 0:
                return {"error": "bdata must be a non-empty string"}
            
            # 验证引用字符串格式
            citations = [line.strip() for line in bdata.strip().split('\n') if line.strip()]
            for citation in citations:
                if not self._validate_citation_string(citation):
                    return {"error": f"Invalid citation format: {citation[:50]}..."}
            
            # 构建ecitmatch参数 - 固定使用文本格式
            ecitmatch_params = {
                'bdata': bdata.strip(),
                'retmode': 'text'  # 固定使用文本格式
            }
            
            # 重试机制
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    handle = Entrez.ecitmatch(**ecitmatch_params)
                    
                    # 读取文本格式结果
                    result = handle.read()
                    if isinstance(result, bytes):
                        result = result.decode('utf-8')
                    handle.close()
                    return {"result": result}
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1 and ("HTTP Error 429" in str(retry_e) or "URLError" in str(retry_e)):
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                    
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 400" in error_msg:
                error_msg = "Invalid citation format. Check your citation strings."
            elif "URLError" in error_msg:
                error_msg = "Network error. Please check your internet connection."
            
            return {"error": f"NCBI ECitMatch failed: {error_msg}"}
