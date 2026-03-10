"""
Tool for paper recommendations using Semantic Scholar API.

Get paper recommendations based on a list of papers.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class SemanticScholarRecommendPapersTool(Tool):
    """
    Tool for paper recommendations using Semantic Scholar API.
    
    Description:
        Get paper recommendations based on a list of papers.
        Uses collaborative filtering and content-based recommendations.
    
    Input Parameters:
        - papers (list, required): List of paper IDs to base recommendations on
        - limit (int, optional): Maximum number of recommendations (default: 10)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object with recommended papers
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get paper recommendations using Semantic Scholar API."""
        import time
        
        # 获取论文列表
        papers = params.get('papers', [])
        if not papers:
            return {"error": "No papers provided"}
        
        # 使用第一个论文ID获取推荐
        paper_id = papers[0]
        base_url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}"
        
        # 构建查询参数
        query_params = {}
        if 'limit' in params:
            query_params['limit'] = params['limit']
        
        if query_params:
            url = f"{base_url}?{urlencode(query_params)}"
        else:
            url = base_url
        
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
        time.sleep(random.uniform(1, 100))  # 减少延迟到0.1-0.5秒
        
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
                    base_delay = 1 + (attempt * 10)  # 基础延迟：1s, 3s, 5s, 7s, 9s
                    delay = base_delay + random.uniform(0, base_delay * 0.5)  # 添加随机因子
                    time.sleep(delay)
                    continue
                    
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"{str(e)} (after {max_retries} attempts)"}
                else:
                    # 等待后重试 - 随机递增延迟以应对API限制
                    base_delay = 1 + (attempt * 2)  # 基础延迟：1s, 3s, 5s, 7s, 9s
                    delay = base_delay + random.uniform(0, base_delay * 0.5)  # 添加随机因子
                    time.sleep(delay)
                    continue
        return {"error": "Max retries exceeded"}
