"""
NCBI Entrez数据库信息工具

使用BioPython的Bio.Entrez.einfo获取数据库信息和统计数据
"""

import json
import os
import time
from typing import Any, Dict

from Bio import Entrez

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class NcbiEntrezEinfoTool(Tool):
    """
    NCBI Entrez数据库信息工具
    
    Description:
        获取NCBI数据库的详细信息，包括字段列表、索引信息、记录数量等元数据。
        可以获取所有可用数据库列表，或特定数据库的详细信息。
    
    Input Parameters:
        - db (str, optional): 数据库名称 - "pubmed", "nucleotide", "protein"等。如果不提供，返回所有可用数据库列表
        - version (str, optional): API版本 - "1.0", "2.0" (默认: "2.0")
    
    Output Format:
        返回数据库信息
        - Success: 直接返回Entrez.read()的结果
        - Error: {"error": "error message"}
    """
    
    def _setup_entrez(self):
        """设置Entrez全局参数"""
        # 尝试从配置文件读取API key和email
        config_file = 'ncbi_key.txt'
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
                pass  # 忽略读取错误，使用默认值

        # Fallback to environment variables
        api_key = api_key or os.getenv("NCBI_API_KEY", "")
        email = email or os.getenv("NCBI_EMAIL", "")

        # 设置email（必需）
        if not hasattr(Entrez, 'email') or not Entrez.email:
            Entrez.email = email if email else "user@example.org"
        
        # 设置API key（可选）
        if api_key and (not hasattr(Entrez, 'api_key') or not Entrez.api_key):
            Entrez.api_key = api_key
    
    def _validate_database(self, db: str) -> bool:
        """验证数据库名称"""
        valid_dbs = {
            'pubmed', 'protein', 'nucleotide', 'nuccore', 'gene', 'genome',
            'structure', 'pmc', 'taxonomy', 'snp', 'geo', 'sra', 'books',
            'cancerchromosomes', 'cdd', 'gap', 'domains', 'genomeprj',
            'gensat', 'gds', 'homologene', 'journals', 'mesh', 'ncbisearch',
            'nlmcatalog', 'omia', 'omim', 'popset', 'probe', 'proteinclusters',
            'pcassay', 'pccompound', 'pcsubstance', 'toolkit', 'unigene', 'unists'
        }
        return db.lower() in valid_dbs
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行NCBI Entrez数据库信息查询"""
        try:
            # 设置Entrez参数
            self._setup_entrez()
            
            # 构建查询参数
            einfo_params = {}
            
            # 添加可选参数并验证
            if 'db' in params:
                db = params['db']
                if not self._validate_database(db):
                    return {"error": f"Invalid database: {db}"}
                einfo_params['db'] = db
            
            if 'version' in params:
                einfo_params['version'] = params['version']
            
            # 执行EInfo查询（带重试机制）
            max_retries = 3
            retry_delay = 1  # 秒
            
            for attempt in range(max_retries):
                try:
                    handle = Entrez.einfo(**einfo_params)
                    record = Entrez.read(handle)
                    handle.close()
                    return record
                except Exception as retry_e:
                    if attempt < max_retries - 1:  # 不是最后一次尝试
                        if "HTTP Error 429" in str(retry_e) or "URLError" in str(retry_e):
                            time.sleep(retry_delay * (attempt + 1))  # 递增延迟
                            continue
                    raise retry_e  # 重新抛出异常让外层处理
            return {"error": "Max retries exceeded"}
            
        except Exception as e:
            error_msg = str(e)
            if "HTTP Error 400" in error_msg:
                error_msg = "Invalid parameters. Check your inputs."
            elif "URLError" in error_msg:
                error_msg = "Network error. Please check your internet connection."
            return {"error": f"NCBI EInfo failed: {error_msg}"}
