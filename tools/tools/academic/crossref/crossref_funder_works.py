"""
Tool for retrieving works associated with a specific funder.

Returns list of works funded by a specified funder organization.
"""

import json
import requests
from typing import Any, Dict
from urllib.parse import urlencode

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefFunderWorksTool(Tool):
    """
    Tool for retrieving works associated with a specific funder.
    
    Description:
        Returns list of works funded by a specified funder organization.
        Supports query, filter, facet, sorting, and pagination capabilities.
    
    Input Parameters:
        - funder_id (str, required): The ID of the funder
        - rows (int, optional): Number of rows per page
        - order (str, optional): Sort order (asc, desc)
        - facet (str, optional): Facet field for counts
        - sample (int, optional): Return N randomly sampled items
        - sort (str, optional): Sort field
        - offset (int, optional): Number of rows to skip
        - mailto (str, optional): Email for polite pool access
        - select (str, optional): Comma-separated fields to return
        - query (str, optional): Free text search query
        - filter (str, optional): Comma-separated filters
        - cursor (str, optional): Cursor for deep paging
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing works list
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve works for specific funder from Crossref."""
        import time
        
        funder_id = params.get("funder_id")
        if not funder_id:
            return {"error": "funder_id parameter is required"}
        
        base_url = f"https://api.crossref.org/funders/{funder_id}/works"
        query_params = {k: v for k, v in params.items() if k != "funder_id" and v is not None}
        
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
