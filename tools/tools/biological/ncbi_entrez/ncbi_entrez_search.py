"""
NCBI Entrez搜索工具

使用BioPython的Bio.Entrez.esearch进行数据库搜索
"""

import json
import os
import time
from typing import Any, Dict

from Bio import Entrez

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class NcbiEntrezSearchTool(Tool):
    """
    NCBI Entrez数据库搜索工具
    
    Description:
        搜索NCBI的各种数据库(PubMed、GenBank、Protein等)，返回匹配的ID列表。
        使用BioPython库确保高稳定性和自动限流。
    
    Input Parameters:
        - db (str, required): 数据库名称 - "pubmed", "nucleotide", "protein", "gene", "genome", "structure"等
        - term (str, required): 搜索查询字符串，支持NCBI搜索语法
        - retmax (int, optional): 最大返回结果数 (默认: 20, 最大: 100000)
        - retstart (int, optional): 起始索引，用于分页 (默认: 0)
        - sort (str, optional): 排序方式 - "relevance", "pub_date", "author", "journal"
        - rettype (str, optional): 返回类型 - "uilist" (默认), "count" (仅返回计数)
        - datetype (str, optional): 日期类型 - "mdat", "pdat", "edat" (仅当使用日期过滤时需要)
        - mindate (str, optional): 最小日期 - YYYY, YYYY/MM, YYYY/MM/DD
        - maxdate (str, optional): 最大日期 - YYYY, YYYY/MM, YYYY/MM/DD
    
    Output Format:
        返回搜索结果
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
        """执行NCBI Entrez数据库搜索"""
        try:
            # 设置Entrez参数
            self._setup_entrez()
            
            # 提取必需参数
            db = params.get('db')
            term = params.get('term')
            
            if not db:
                return {"error": "Missing required parameter: db"}
            
            if not self._validate_database(db):
                return {"error": f"Invalid database: {db}"}
            
            if not term:
                return {"error": "Missing required parameter: term"}
            
            # 构建查询参数
            search_params = {
                'db': db,
                'term': term
            }
            
            # 添加可选参数并验证
            if 'retmax' in params:
                retmax = params['retmax']
                if not isinstance(retmax, int) or retmax < 1 or retmax > 100000:
                    return {"error": "Parameter 'retmax' must be an integer between 1 and 100000"}
                search_params['retmax'] = retmax
            
            if 'retstart' in params:
                retstart = params['retstart']
                if not isinstance(retstart, int) or retstart < 0:
                    return {"error": "Parameter 'retstart' must be a non-negative integer"}
                search_params['retstart'] = retstart
            
            # 其他参数直接传递，让BioPython验证
            for param in ['sort', 'rettype', 'datetype', 'mindate', 'maxdate']:
                if param in params:
                    search_params[param] = params[param]
            
            # 执行ESearch查询（带重试机制）
            max_retries = 3
            retry_delay = 1  # 秒
            
            for attempt in range(max_retries):
                try:
                    handle = Entrez.esearch(**search_params)
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
                error_msg = "Invalid query syntax. Check your search terms."
            elif "URLError" in error_msg:
                error_msg = "Network error. Please check your internet connection."
            return {"error": f"NCBI ESearch failed: {error_msg}"}
