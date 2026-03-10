"""
Tool for getting Rxterms version information.

This tool retrieves the current version of the Rxterms dataset.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxtermsGetRxtermsVersionTool(Tool):
    """
    Tool for getting Rxterms version information.
    
    Description:
        Retrieve the current version of the Rxterms dataset using the RxNAV REST API.
        Returns version information and release details.
    
    Input Parameters:
        No required parameters.
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing version information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get Rxterms version information."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/RxTerms/version.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for Rxterms version")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
