"""
Tool for retrieving specific journal information by ISSN.

Get detailed metadata for a journal using its ISSN identifier.
"""

import json
import requests
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CrossrefGetJournalTool(Tool):
    """
    Tool for retrieving specific journal information by ISSN.
    
    Description:
        Get detailed metadata for a journal using its ISSN identifier.
        Returns comprehensive journal information including publisher, subjects, and statistics.
    
    Input Parameters:
        - issn (str, required): The ISSN identifier of the journal
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing journal metadata
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve specific journal by ISSN from Crossref."""
        import time
        
        issn = params.get("issn")
        if not issn:
            return {"error": "issn parameter is required"}
        
        url = f"https://api.crossref.org/journals/{issn}"
        
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
