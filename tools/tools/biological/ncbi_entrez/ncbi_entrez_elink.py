"""
NCBI Entrez关联查找工具

使用BioPython的Bio.Entrez.elink查找数据库记录之间的关联
"""

import json
import os
import time
from typing import Any, Dict

from Bio import Entrez

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class NcbiEntrezElinkTool(Tool):
    """
    NCBI Entrez记录关联查找工具
    
    Description:
        查找NCBI数据库记录之间的关联关系，如PubMed文章的相关文章、
        基因与蛋白质的关联、序列与文献的关联等。支持多种链接类型。
    
    Input Parameters:
        - dbfrom (str, required): 源数据库名称 - "pubmed", "nucleotide", "protein"等
        - db (str, required): 目标数据库名称 - "pubmed", "nucleotide", "protein"等
        - id (str, required): 源记录ID(s)，多个ID用逗号分隔
        - linkname (str, optional): 链接类型名称，如"pubmed_pubmed", "pubmed_protein"等
        - term (str, optional): 过滤查询词，用于筛选关联结果
        - holding (str, optional): 机构代码，用于筛选特定机构的资源
        - datetype (str, optional): 日期类型 - "mdat", "pdat", "edat"
        - reldate (int, optional): 相对日期天数，获取指定天数内的关联
        - mindate (str, optional): 最小日期 - YYYY, YYYY/MM, YYYY/MM/DD
        - maxdate (str, optional): 最大日期 - YYYY, YYYY/MM, YYYY/MM/DD
        - cmd (str, optional): 命令类型 - "neighbor" (默认), "neighbor_score", "acheck", "ncheck", "lcheck", "llinks", "llinkslib", "prlinks"
    
    Output Format:
        返回关联查找结果
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
        """执行NCBI Entrez关联查找"""
        try:
            # 设置Entrez参数
            self._setup_entrez()
            
            # 提取必需参数
            dbfrom = params.get('dbfrom')
            db = params.get('db')
            id_param = params.get('id')
            
            if not dbfrom:
                return {"error": "Missing required parameter: dbfrom"}
            
            if not self._validate_database(dbfrom):
                return {"error": f"Invalid source database: {dbfrom}"}
            
            if not db:
                return {"error": "Missing required parameter: db"}
            
            if not self._validate_database(db):
                return {"error": f"Invalid target database: {db}"}
            
            if not id_param:
                return {"error": "Missing required parameter: id"}
            
            # 构建查询参数
            elink_params = {
                'dbfrom': dbfrom,
                'db': db,
                'id': id_param
            }
            
            # 添加可选参数并验证
            if 'reldate' in params:
                reldate = params['reldate']
                if not isinstance(reldate, int) or reldate < 0:
                    return {"error": "Parameter 'reldate' must be a non-negative integer"}
                elink_params['reldate'] = reldate
            
            # 其他参数直接传递，让BioPython验证
            for param in ['linkname', 'term', 'holding', 'datetype', 'mindate', 'maxdate', 'cmd']:
                if param in params:
                    elink_params[param] = params[param]
            
            # 执行ELink查询（带重试机制）
            max_retries = 3
            retry_delay = 1  # 秒
            
            for attempt in range(max_retries):
                try:
                    handle = Entrez.elink(**elink_params)
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
                error_msg = "Invalid parameters or ID. Check your inputs."
            elif "URLError" in error_msg:
                error_msg = "Network error. Please check your internet connection."
            return {"error": f"NCBI ELink failed: {error_msg}"}
