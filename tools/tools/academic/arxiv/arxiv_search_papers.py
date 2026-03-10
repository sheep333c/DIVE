"""
Tool for general paper search on arXiv.

Basic paper search functionality across all fields and metadata.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class ArxivSearchPapersTool(Tool):
    """
    Tool for general paper search on arXiv.
    
    Description:
        Basic paper search functionality across all fields and metadata.
        Searches through titles, abstracts, authors, and other paper data.
    
    Input Parameters:
        - search_query (str, required): Search query string
        - start (int, optional): Starting index for results (default: 0)
        - max_results (int, optional): Maximum number of results (default: 10)
        - sortBy (str, optional): Sort by relevance, lastUpdatedDate, submittedDate
        - sortOrder (str, optional): ascending or descending
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: XML string containing search results
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search arXiv papers with general query."""
        import time
        
        # 构建URL - 直接使用所有参数
        base_url = "https://export.arxiv.org/api/query"
        url = f"{base_url}?{urlencode(params)}"
        
        # 重试3次
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urlopen(url) as response:
                    # 直接返回API的原始响应
                    content = response.read().decode('utf-8')
                    return content
                    
            except HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.code}: {e.reason} (after {max_retries} attempts)"}
                else:
                    # 等待后重试
                    time.sleep(1 * (attempt + 1))  # 递增等待时间
                    continue
                    
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"{str(e)} (after {max_retries} attempts)"}
                else:
                    # 等待后重试
                    time.sleep(1 * (attempt + 1))  # 递增等待时间
                    continue
        return {"error": "Max retries exceeded"}
