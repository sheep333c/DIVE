"""
Tool for analyzing text using OpenAlex's aboutness endpoint.

Analyzes text to find related topics and concepts.
"""

import json
import time
import random
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class OpenalexAnalyzeTextTool(Tool):
    """
    Tool for accessing OpenAlex text analysis endpoint.
    
    Description:
        Access OpenAlex text API endpoint directly.
        All parameters are passed through to the API without modification.
    
    Input Parameters:
        All parameters are passed directly to the OpenAlex API.
        Common parameters may include text, abstract, return_topics, etc.
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON string containing API response
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
        
    Design Philosophy:
        Pure pass-through - API returns what, the tool returns directly.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text using OpenAlex aboutness endpoint."""
        max_retries = 10  # 设置最大重试次数为10次
        
        for attempt in range(max_retries):
            try:
                # 构建URL - 直接使用所有参数
                base_url = "https://api.openalex.org/text"
                url = f"{base_url}?{urlencode(params)}"
                
                with urlopen(url) as response:
                    # 直接返回API的原始响应
                    return response.read().decode('utf-8')
                    
            except HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.code}: {e.reason}"}
                else:
                    # 等待后重试，使用递增延迟 + 随机延迟避免同时重试
                    base_delay = 5 * (attempt + 1)
                    random_delay = random.uniform(0.5, 2.0)
                    time.sleep(base_delay + random_delay)
                    continue
            except Exception as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": str(e)}
                else:
                    # 等待后重试，使用递增延迟 + 随机延迟避免同时重试
                    base_delay = 5 * (attempt + 1)
                    random_delay = random.uniform(0.5, 2.0)
                    time.sleep(base_delay + random_delay)
                    continue
        
        # 如果所有重试都失败了，返回通用错误
        return {"error": "Max retries exceeded"}
