"""
Tool for retrieving a specific institution from OpenAlex by ID.

Fetches complete institution information using OpenAlex identifiers.
"""

import json
import time
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class OpenalexGetInstitutionTool(Tool):
    """
    Tool for retrieving institutions from OpenAlex.
    
    Description:
        Access OpenAlex institutions API endpoint directly.
        All parameters are passed through to the API without modification.
    
    Input Parameters:
        All parameters are passed directly to the OpenAlex API.
        Common parameters include filters, search queries, pagination, etc.
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON string containing API response
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
        
    Design Philosophy:
        Pure pass-through - API returns what, the tool returns directly.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve OpenAlex institution by ID."""
        import time
        from urllib.request import Request
        
        # 提取institution_id
        institution_id = params.get('institution_id')
        if not institution_id:
            return {"error": "'institution_id' is required"}
        
        # 构建URL - 使用institution_id作为路径参数
        base_url = f"https://api.openalex.org/institutions/{institution_id}"
        
        # 准备其他查询参数
        other_params = {k: v for k, v in params.items() if k != 'institution_id'}
        if other_params:
            url = f"{base_url}?{urlencode(other_params)}"
        else:
            url = base_url
        
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
