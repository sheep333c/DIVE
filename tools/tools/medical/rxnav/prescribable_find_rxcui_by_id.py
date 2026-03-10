"""
Tool for finding prescribable drug concepts by identifier.

This tool searches for RxCUI identifiers based on various types of drug identifiers
like NDC codes, UNII codes, etc.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableFindRxcuiByIdTool(Tool):
    """
    Tool for finding prescribable drug concepts by identifier.
    
    Description:
        Search for RxCUI identifiers based on various types of drug identifiers
        like NDC codes, UNII codes, etc. using the RxNAV REST API.
    
    Input Parameters:
        - idtype (str, required): Type of identifier (e.g., NDC, UNII, RXCUI)
        - id (str, required): The identifier value to search for
        - allsrc (int, optional): Scope of search (0=Active, 1=Current)
        - srclist (str, optional): Space-separated list of source vocabularies
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing the drug concept data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search for prescribable drug concepts by identifier."""
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
