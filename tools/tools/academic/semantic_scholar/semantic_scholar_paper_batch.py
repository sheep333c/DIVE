"""
Tool for batch retrieval of papers from Semantic Scholar by IDs.

Get details for multiple papers at once using POST request.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class SemanticScholarPaperBatchTool(Tool):
    """
    Tool for batch retrieval of papers from Semantic Scholar by IDs.
    
    Description:
        Get details for multiple papers at once using POST request.
        Supports up to 500 paper IDs per request.
        Fields parameter is passed as query parameter, not in POST body.
    
    Input Parameters:
        - ids (list, required): List of paper IDs to retrieve
        - fields (str, optional): Comma-separated list of fields to return
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON array containing paper details
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Batch retrieve papers using Semantic Scholar API."""
        import time
        
        # 构建URL
        base_url = "https://api.semanticscholar.org/graph/v1/paper/batch"
        
        # 提取ids和fields
        ids = params.get('ids', [])
        fields = params.get('fields')
        
        # 构建查询参数
        query_params = {}
        if fields:
            query_params['fields'] = fields
        
        if query_params:
            url = f"{base_url}?{urlencode(query_params)}"
        else:
            url = base_url
        
        # 准备请求数据
        data = {"ids": ids}
        json_data = json.dumps(data).encode('utf-8')
        
        # 准备请求头
        headers = {
            'User-Agent': 'VerifiableTools/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # 添加API key（如果提供）
        if context.auth and 'api_key' in context.auth:
            headers['x-api-key'] = context.auth['api_key']
        
        request = Request(url, data=json_data, headers=headers, method='POST')
        
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
