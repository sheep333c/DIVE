"""
TogoWS条目获取工具。

此工具使用TogoWS Web服务从各种生物信息学数据库获取特定条目。
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TogoWSEntryTool(Tool):
    """
    TogoWS条目获取工具。
    
    使用Bio.TogoWS从指定数据库获取特定ID的条目数据。
    支持多种输出格式和数据库。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行TogoWS条目获取。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - database (str): 数据库名称 (如 "uniprot", "ncbi-pubmed")
                - entry_id (str): 条目ID
                - format (str): 输出格式 (如 "fasta", "xml", "json")
                - field (str, 可选): 特定字段
        
        Returns:
            包含条目数据的字典
        """
        try:
            from Bio import TogoWS
            
            # 提取参数
            database = params.get('database', '')
            entry_id = params.get('entry_id', '')
            format_type = params.get('format', 'fasta')
            field = params.get('field')
            
            # 验证输入
            if not database:
                return {"error": "数据库参数是必需的"}
            
            if not entry_id:
                return {"error": "条目ID参数是必需的"}
            
            # 执行带重试机制的请求
            max_retries = 3
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 调用TogoWS条目获取
                    with TogoWS.entry(database, entry_id, format=format_type, field=field) as handle:
                        return handle.read()
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        if "timeout" in str(retry_e).lower() or "URLError" in str(retry_e):
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            return {"error": str(e)}
