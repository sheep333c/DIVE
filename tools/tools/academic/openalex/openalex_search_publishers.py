"""
Tool for searching publishers on OpenAlex.

Basic search functionality for academic publishers and publishing organizations.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class OpenalexSearchPublishersTool(Tool):
    """
    Tool for searching publishers on OpenAlex.
    
    Description:
        Search for academic publishers and publishing organizations.
        Searches through publisher names and alternative names.
    
    Input Parameters:
        - search (str, optional): Search query string for publisher names
        - filter (str, optional): Filter criteria (e.g., "country_codes:us", "sources_count:>100")
        - sort (str, optional): Sort order (e.g., "sources_count:desc", "works_count:desc")
        - per-page (int, optional): Number of results per page (default: 25)
        - page (int, optional): Page number for pagination (default: 1)
        - select (str, optional): Comma-separated list of fields to return
        - mailto (str, optional): Email for polite pool (higher rate limits)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON string containing publishers data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search OpenAlex publishers."""
        import time
        from urllib.request import Request
        
        # 构建URL - 使用所有参数作为查询参数
        base_url = "https://api.openalex.org/publishers"
        url = f"{base_url}?{urlencode(params)}"
        
        # 准备请求头
        headers = {
            'User-Agent': 'VerifiableTools/1.0 (https://github.com/your-org/verifiable-tools)',
            'Accept': 'application/json'
        }
        
        request = Request(url, headers=headers)
        
        # 添加随机延迟以避免过于频繁的请求
        import random
        time.sleep(random.uniform(1, 3))
        
        # 设置代理
        import os
        proxy_handler = None
        if os.environ.get('http_proxy') or os.environ.get('https_proxy'):
            from urllib.request import ProxyHandler, build_opener
            proxy_handler = ProxyHandler({
                'http': os.environ.get('http_proxy', ''),
                'https': os.environ.get('https_proxy', '')
            })
            opener = build_opener(proxy_handler)
        else:
            opener = urlopen
        
        max_retries = 5  # 设置最大重试次数为5次
        
        for attempt in range(max_retries):
            try:
                if proxy_handler:
                    with opener.open(request) as response:
                        # 直接返回API的原始响应
                        content = response.read().decode('utf-8')
                        return json.loads(content)
                else:
                    with urlopen(request) as response:
                        # 直接返回API的原始响应
                        content = response.read().decode('utf-8')
                        return json.loads(content)
                    
            except HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.code}: {e.reason} (after {max_retries} attempts)"}
                else:
                    # 等待后重试 - 随机递增延迟以应对API限制
                    base_delay = 1 + (attempt * 2)  # 基础延迟：1s, 3s, 5s, 7s, 9s
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
        
        # 如果所有重试都失败了，返回通用错误
        return {"error": "Max retries exceeded"}
