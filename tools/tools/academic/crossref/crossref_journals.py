"""
Tool for retrieving journals from the Crossref database.

Returns list of journals with query and pagination support.
"""

import json
import requests
from typing import Any, Dict
from urllib.parse import urlencode

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefJournalsTool(Tool):
    """
    Tool for retrieving journals from the Crossref database.
    
    Description:
        Returns list of journals in the Crossref database with free text search
        and pagination capabilities.
    
    Input Parameters:
        - cursor (str, optional): Cursor for deep paging
        - query (str, optional): Free text search query
        - rows (int, optional): Number of rows per page
        - mailto (str, optional): Email for polite pool access
        - offset (int, optional): Number of rows to skip
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing journals list
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve journals list from Crossref."""
        import time
        
        base_url = "https://api.crossref.org/journals"
        query_params = {k: v for k, v in params.items() if v is not None}
        
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
