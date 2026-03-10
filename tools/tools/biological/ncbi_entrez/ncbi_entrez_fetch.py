"""
NCBI Entrez获取工具

使用BioPython的Bio.Entrez.efetch获取完整记录
"""

import json
import os
import time
from typing import Any, Dict

from Bio import Entrez

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class NcbiEntrezFetchTool(Tool):
    """
    NCBI Entrez记录获取工具

    Description:
        从NCBI数据库获取完整记录，支持多种格式（XML、FASTA、GenBank等）。
        使用BioPython库确保高稳定性和自动限流。

    Input Parameters:
        - db (str, required): 数据库名称 - "pubmed", "nucleotide", "protein", "gene", "genome", "structure"等
        - id (str, required): 记录ID，支持单个ID或逗号分隔的多个ID
        - rettype (str, optional): 返回类型 - "xml", "fasta", "gb", "abstract", "medline"等
        - retmode (str, optional): 返回模式 - "xml", "text", "json"等
        - retstart (int, optional): 起始索引，用于分页 (默认: 0)
        - retmax (int, optional): 最大返回结果数 (默认: 20, 最大: 10000)
        - strand (int, optional): DNA链方向 - 1 (plus), 2 (minus)
        - seq_start (int, optional): 序列起始位置
        - seq_stop (int, optional): 序列结束位置
        - complexity (int, optional): 序列复杂度 - 0 (whole), 1 (bioseq), 2 (bioseq-set)

    Output Format:
        返回获取的记录数据
        - Success: 直接返回记录数据（字符串格式）
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

    def _parse_ids(self, id_param: str) -> list:
        """解析ID参数，支持单个ID或逗号分隔的多个ID"""
        if isinstance(id_param, (list, tuple)):
            return [str(i).strip() for i in id_param if str(i).strip()]
        
        id_str = str(id_param).strip()
        if ',' in id_str:
            return [i.strip() for i in id_str.split(',') if i.strip()]
        else:
            return [id_str] if id_str else []

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行NCBI Entrez记录获取"""
        try:
            # 设置Entrez参数
            self._setup_entrez()
            
            # 提取必需参数
            db = params.get('db')
            id_param = params.get('id')
            
            if not db:
                return {"error": "Missing required parameter: db"}
            
            if not self._validate_database(db):
                return {"error": f"Invalid database: {db}"}
            
            if not id_param:
                return {"error": "Missing required parameter: id"}
            
            # 构建查询参数
            fetch_params = {
                'db': db,
                'id': id_param
            }
            
            # 添加可选参数并验证
            if 'retstart' in params:
                retstart = params['retstart']
                if not isinstance(retstart, int) or retstart < 0:
                    return {"error": "Parameter 'retstart' must be a non-negative integer"}
                fetch_params['retstart'] = retstart
            
            if 'retmax' in params:
                retmax = params['retmax']
                if not isinstance(retmax, int) or retmax < 1 or retmax > 10000:
                    return {"error": "Parameter 'retmax' must be an integer between 1 and 10000"}
                fetch_params['retmax'] = retmax
            
            # 其他参数直接传递，让BioPython验证
            for param in ['rettype', 'retmode', 'strand', 'seq_start', 'seq_stop', 'complexity']:
                if param in params:
                    fetch_params[param] = params[param]
            
            # 执行EFetch查询（带重试机制）
            max_retries = 3
            retry_delay = 1  # 秒
            
            for attempt in range(max_retries):
                try:
                    handle = Entrez.efetch(**fetch_params)
                    data = handle.read()
                    handle.close()
                    
                    # 处理二进制数据
                    if isinstance(data, bytes):
                        try:
                            data = data.decode('utf-8')
                        except UnicodeDecodeError:
                            data = data.decode('latin-1')
                    
                    return data
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
                error_msg = "Invalid parameters or ID. Check your inputs."
            elif "URLError" in error_msg:
                error_msg = "Network error. Please check your internet connection."
            return {"error": f"NCBI EFetch failed: {error_msg}"}
