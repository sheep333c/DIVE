"""
TogoWS数据库搜索工具。

此工具使用TogoWS Web服务在生物信息学数据库中执行搜索。
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TogoWSSearchTool(Tool):
    """
    TogoWS数据库搜索工具。
    
    使用Bio.TogoWS在指定数据库中执行搜索查询，
    支持分页和多种输出格式。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行TogoWS数据库搜索。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - database (str): 数据库名称 (如 "uniprot", "ncbi-pubmed")
                - query (str): 搜索查询字符串
                - offset (int, 可选): 结果偏移量 (默认1)
                - limit (int, 可选): 结果限制数量 (默认10)
        
        Returns:
            包含搜索结果的字典
        """
        try:
            from Bio import TogoWS
            
            # 提取参数
            database = params.get('database', '')
            query = params.get('query', '')
            offset = params.get('offset', 1)  # TogoWS要求offset至少为1
            limit = params.get('limit', 10)
            # 固定使用JSON格式
            format_type = 'json'
            
            # 验证输入
            if not database:
                return {"error": "数据库参数是必需的"}
            
            if not query:
                return {"error": "查询参数是必需的"}
            
            # 验证offset和limit参数 (TogoWS要求offset >= 1)
            if offset < 1:
                return {"error": "偏移量必须大于等于1"}
            
            if limit <= 0:
                return {"error": "限制数量必须大于0"}
            
            # 执行带重试机制的请求
            max_retries = 3
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 调用TogoWS搜索 (使用位置参数: db, query, offset, limit, format)
                    with TogoWS.search(database, query, offset=offset, limit=limit, format=format_type) as handle:
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
