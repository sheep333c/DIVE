"""
Tool for getting approximate match information for Rxnorm concepts.

This tool retrieves approximate matching drug concepts for a given drug name.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormGetApproximateMatchTool(Tool):
    """
    Tool for getting approximate match information for Rxnorm concepts.
    
    Description:
        Retrieve approximate matching drug concepts for a given drug name using the RxNAV REST API.
        Returns concepts that are similar but not exact matches.
    
    Input Parameters:
        - term (str, required): Drug name or term to search for
        - maxEntries (int, optional): Maximum number of entries to return
        - option (int, optional): Search option (0=starts with, 1=contains)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing approximate matches
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get approximate match information for Rxnorm concepts."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/approximateTerm.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for approximate match")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
