"""
Tool for paper bulk search using Semantic Scholar API.

Bulk retrieval of basic paper data without search relevance.
Supports boolean logic queries and various filters.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class SemanticScholarPaperBulkSearchTool(Tool):
    """
    Tool for paper bulk search using Semantic Scholar API.
    
    Description:
        Bulk retrieval of basic paper data without search relevance.
        Supports boolean logic queries and various filters.
        Returns up to 1,000 papers per call with continuation tokens.
    
    Input Parameters:
        - query (str, required): Text query with boolean logic support
        - token (str, optional): Continuation token for pagination
        - fields (str, optional): Comma-separated list of fields to return
        - sort (str, optional): Sort by paperId, publicationDate, or citationCount
        - publicationTypes (str, optional): Filter by publication types
        - openAccessPdf (str, optional): Filter for papers with public PDF
        - minCitationCount (str, optional): Minimum number of citations
        - publicationDateOrYear (str, optional): Publication date range
        - year (str, optional): Publication year range
        - venue (str, optional): Publication venues
        - fieldsOfStudy (str, optional): Fields of study
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object with total, token, and data fields
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Bulk search papers using Semantic Scholar API."""
        import time
        
        # 构建URL
        base_url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
        url = f"{base_url}?{urlencode(params)}"
        
        # 准备请求头
        headers = {
            'User-Agent': 'VerifiableTools/1.0',
            'Accept': 'application/json'
        }
        
        # 添加API key（如果提供）
        if context.auth and 'api_key' in context.auth:
            headers['x-api-key'] = context.auth['api_key']
        
        request = Request(url, headers=headers)
        
        # 添加随机延迟以避免过于频繁的请求
        import random
        time.sleep(random.uniform(1, 100))
        
        # 重试5次
        max_retries = 5
        for attempt in range(max_retries):
            try:
                with urlopen(request) as response:
                    # 直接返回API的原始响应
                    content = response.read().decode('utf-8')
                    return json.loads(content)
                    
            except HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.code}: {e.reason} (after {max_retries} attempts)"}
                else:
                    # 等待后重试 - 随机递增延迟以应对API限制
                    base_delay = 1 + (attempt * 10)  # 基础延迟：1s, 11s, 21s, 31s, 41s
                    delay = base_delay + random.uniform(0, base_delay * 0.5)  # 添加随机因子
                    time.sleep(delay)
                    continue
                    
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"{str(e)} (after {max_retries} attempts)"}
                else:
                    # 等待后重试 - 随机递增延迟以应对API限制
                    base_delay = 1 + (attempt * 10)  # 基础延迟：1s, 11s, 21s, 31s, 41s
                    delay = base_delay + random.uniform(0, base_delay * 0.5)  # 添加随机因子
                    time.sleep(delay)
                    continue
        return {"error": "Max retries exceeded"}
