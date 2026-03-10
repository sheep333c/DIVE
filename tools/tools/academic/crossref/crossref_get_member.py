"""
Tool for retrieving specific member information by ID.

Get detailed metadata for a specific Crossref member organization.
"""

import json
import requests
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefGetMemberTool(Tool):
    """
    Tool for retrieving specific member information by ID.
    
    Description:
        Get detailed metadata for a specific Crossref member organization 
        including names, locations, DOI counts, and prefix information.
    
    Input Parameters:
        - member_id (int, required): The identifier of the member to retrieve
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing member metadata
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve specific member by ID from Crossref."""
        import time
        
        member_id = params.get("id")
        if not member_id:
            return {"error": "id parameter is required"}
        
        url = f"https://api.crossref.org/members/{member_id}"
        
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
