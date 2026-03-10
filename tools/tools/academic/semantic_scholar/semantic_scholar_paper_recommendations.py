"""
Tool for getting paper recommendations for a specific paper using Semantic Scholar API.

Get recommendations for a specific paper by its ID.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class SemanticScholarPaperRecommendationsTool(Tool):
    """
    Tool for getting paper recommendations for a specific paper using Semantic Scholar API.
    
    Description:
        Get recommendations for a specific paper by its ID.
        Returns papers similar to the given paper.
    
    Input Parameters:
        - paper_id (str, required): Paper identifier for which to get recommendations
        - limit (int, optional): Maximum number of recommendations (default: 10)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object with recommended papers
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get paper recommendations using Semantic Scholar API."""
        import time
        
        # 提取paper_id并构建URL
        paper_id = params.get('paper_id')
        if not paper_id:
            return {"error": "'paper_id' is required"}
        base_url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}"
        
        # 如果有其他参数，添加到查询字符串
        if params:
            url = f"{base_url}?{urlencode(params)}"
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
        time.sleep(random.uniform(1, 100))  # 增加延迟以避免代理连接问题
        
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
