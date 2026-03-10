"""
Tool for finding prescribable drug concepts by name with various precision levels.

This tool searches for RxCUI identifiers based on drug names using exact, 
normalized, or approximate matching methods.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableFindRxcuiByStringTool(Tool):
    """
    Tool for finding prescribable drug concepts by name with various precision levels.
    
    Description:
        Search for RxCUI identifiers based on drug names using the RxNAV REST API.
        Supports exact, normalized, or approximate matching methods for prescribable concepts.
    
    Input Parameters:
        - name (str, required): Name of concept to find
        - allsrc (int, optional): Scope of search (0=Active, 1=Current)
        - srclist (str, optional): Space-separated list of source vocabularies
        - search (int, optional): Precision (0=Exact, 1=Normalized, 2=Exact or Normalized, 9=Approximate)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing the drug concept data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for prescribable drug concepts by name."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://rxnav.nlm.nih.gov/REST/Prescribe/rxcui.json"
            url = f"{base_url}?{urlencode(params)}"
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
