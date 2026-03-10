"""
Tool for getting all Rxterms information.

This tool retrieves comprehensive Rxterms information for a given RxCUI.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxtermsGetAllRxtermInfoTool(Tool):
    """
    Tool for getting all Rxterms information.
    
    Description:
        Retrieve comprehensive Rxterms information for a given RxCUI using the RxNAV REST API.
        Returns detailed Rxterms data including display names and other attributes.
    
    Input Parameters:
        - rxcui (str, required): Rxnorm Concept Unique Identifier
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing Rxterms information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get all Rxterms information for a given RxCUI."""
        try:
            # 构建URL - rxcui在路径中，其他参数作为查询参数
            rxcui = params.get("rxcui", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/RxTerms/rxcui/{rxcui}/allinfo.json"
            
            # 过滤掉rxcui参数，构建查询参数
            query_params = {k: v for k, v in params.items() if k != "rxcui" and v}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for all Rxterms info")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
