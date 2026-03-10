"""
TogoWS搜索计数工具。

此工具使用TogoWS Web服务获取数据库搜索的结果计数。
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TogoWSSearchCountTool(Tool):
    """
    TogoWS搜索计数工具。
    
    使用Bio.TogoWS获取指定数据库中搜索查询的匹配结果数量。
    支持多种生物信息学数据库。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行TogoWS搜索计数。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - database (str): 数据库名称 (如 "uniprot", "ncbi-pubmed", "ncbi-nucleotide")
                - query (str): 搜索查询字符串
        
        Returns:
            包含搜索计数结果的字典
        """
        try:
            from Bio import TogoWS
            
            # 提取参数
            database = params.get('database', '')
            query = params.get('query', '')
            
            # 验证输入
            if not database:
                return {"error": "数据库参数是必需的"}
            
            if not query:
                return {"error": "查询参数是必需的"}
            
            # 执行带重试机制的请求
            max_retries = 3
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 调用TogoWS搜索计数
                    return TogoWS.search_count(database, query)
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        if "timeout" in str(retry_e).lower() or "URLError" in str(retry_e):
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            return {"error": str(e)}
