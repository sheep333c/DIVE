"""
Tool for filtering Rxnorm concepts by property.

This tool filters drug concepts based on specific property criteria.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormFilterByPropertyTool(Tool):
    """
    Tool for filtering Rxnorm concepts by property.
    
    Description:
        Filter drug concepts based on specific property criteria using the RxNAV REST API.
        Returns concepts that match the specified property filters.
    
    Input Parameters:
        - rxcui (str, required): Rxnorm Concept Unique Identifier
        - propName (str, required): Property name to filter by
        - propValue (str, optional): Property value to match
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing filtered concepts
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Filter Rxnorm concepts by property."""
        try:
            # 构建URL和查询参数
            rxcui = params.get("rxcui", "")
            if not rxcui:
                return {"error": "rxcui parameter is required"}
                
            base_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/filter.json"
            
            # 从参数中移除rxcui，只使用其他参数作为查询参数
            query_params = {k: v for k, v in params.items() if k != 'rxcui' and v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API to filter by property")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
