"""
Tool for retrieving specific funder information by ID.

Get detailed metadata for a funder and its suborganizations by ID.
"""

import json
import requests
from typing import Any, Dict
from urllib.parse import urlencode

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefGetFunderTool(Tool):
    """
    Tool for retrieving specific funder information by ID.
    
    Description:
        Get detailed metadata for a funder and its suborganizations by ID.
    
    Input Parameters:
        - funder_id (str, required): Parameter description
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing response data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute crossref_get_funder request."""
        import time
        
        funder_id = params.get("id")
        if not funder_id:
            return {"error": "id parameter is required"}
        
        base_url = f"https://api.crossref.org/funders/{funder_id}"
        query_params = {k: v for k, v in params.items() if k != "id" and v is not None}
        
        if query_params:
            url = f"{base_url}?{urlencode(query_params)}"
        else:
            url = base_url
        
        headers = {
            'User-Agent': 'VerifiableTools/1.0 (https://github.com/verifiable-tools)',
            'Accept': 'application/json'
        }
        
        # 重试3次
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=60)
                response.raise_for_status()
                
                return response.json()
                    
            except requests.exceptions.HTTPError as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"HTTP {e.response.status_code}: {e.response.reason} (after {max_retries} attempts)"}
                else:
                    # 等待后重试
                    time.sleep(1 * (attempt + 1))  # 递增等待时间
                    continue
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:  # 最后一次尝试
                    return {"error": f"Request error: {str(e)} (after {max_retries} attempts)"}
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
