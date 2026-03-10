"""
Tool for getting NDC properties from Rxnorm.

This tool retrieves NDC property information for given NDC codes.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormGetNdcPropertiesTool(Tool):
    """
    Tool for getting NDC properties from Rxnorm.
    
    Description:
        Retrieve NDC property information for given NDC codes using the RxNAV REST API.
        Returns detailed properties associated with National Drug Codes.
    
    Input Parameters:
        - id (str, required): NDC (CMS 11-digit, or 5-3 or 4-4-2), or RXCUI, or FDA SPL set ID
        - ndcstatus (str, optional): Status filter for NDCs (active, obsolete, alien, ALL)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing NDC properties
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get NDC properties from Rxnorm."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/ndcproperties.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for NDC properties")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
