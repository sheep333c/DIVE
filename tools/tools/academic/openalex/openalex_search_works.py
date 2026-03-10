"""
Tool for searching academic works on OpenAlex.

Basic search functionality for journal articles, books, datasets, and theses.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class OpenalexSearchWorksTool(Tool):
    """
    Tool for searching academic works on OpenAlex.
    
    Description:
        Search for academic works including journal articles, books, datasets, and theses.
        Searches through titles, abstracts, and full text content.
    
    Input Parameters:
        - search (str, optional): Search query string for titles, abstracts, and full text
        - filter (str, optional): Filter criteria (e.g., "publication_year:2023", "is_oa:true")
        - sort (str, optional): Sort field and order (e.g., "cited_by_count:desc")
        - per-page (int, optional): Number of results per page (default: 25)
        - page (int, optional): Page number for pagination (default: 1)
        - select (str, optional): Comma-separated list of fields to return
        - mailto (str, optional): Email for polite pool (higher rate limits)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON string containing search results
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search OpenAlex works."""
        max_retries = 5  # 设置最大重试次数为5次
        
        for attempt in range(max_retries):
            try:
                # 构建URL - 直接使用所有参数
                base_url = "https://api.openalex.org/works"
                url = f"{base_url}?{urlencode(params)}"
                
                with urlopen(url) as response:
                    # 直接返回API的原始响应
                    return response.read().decode('utf-8')
                    
            except HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.code}: {e.reason}"}
                else:
                    # 等待后重试，使用递增延迟
                    time.sleep(5 * (attempt + 1))
                    continue
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": str(e)}
                else:
                    # 等待后重试，使用递增延迟
                    time.sleep(5 * (attempt + 1))
                    continue
        
        # 如果所有重试都失败了，返回通用错误
        return {"error": "Max retries exceeded"}
