"""
Tool for getting display terms for Rxnorm drug concepts.

This tool retrieves display terms for a given RxCUI.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormGetDisplayTermsTool(Tool):
    """
    Tool for getting display terms for Rxnorm drug concepts.
    
    Description:
        Retrieve display terms for a given RxCUI using the RxNAV REST API.
        Returns human-readable display names for drug concepts.
    
    Input Parameters:
        - No parameters required - returns all display terms for auto-completion
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing display terms
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get display terms for an Rxnorm drug concept."""
        try:
            # 构建URL - 不需要任何参数
            base_url = "https://rxnav.nlm.nih.gov/REST/displaynames.json"
            url = base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for display terms")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
