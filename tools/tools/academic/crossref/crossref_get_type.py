"""
Tool for retrieving information about a metadata work type.

Get details about a specific work type by its identifier.
"""

import json
import requests
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefGetTypeTool(Tool):
    """
    Tool for retrieving information about a metadata work type.
    
    Description:
        Get details about a specific work type by its identifier.
        Returns information about work type definitions and labels.
    
    Input Parameters:
        - type_id (str, required): The identifier of the work type
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing type metadata
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve specific type by ID from Crossref."""
        import time
        
        type_id = params.get("id")
        if not type_id:
            return {"error": "id parameter is required"}
        
        url = f"https://api.crossref.org/types/{type_id}"
        
        headers = {
            'User-Agent': 'VerifiableTools/1.0 (https://github.com/verifiable-tools)',
            'Accept': 'application/json'
        }
        
        # 重试5次
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
