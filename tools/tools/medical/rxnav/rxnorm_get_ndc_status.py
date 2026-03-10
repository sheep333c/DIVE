"""
Tool for getting NDC status information from Rxnorm.

This tool retrieves NDC status information for given NDC codes.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormGetNdcStatusTool(Tool):
    """
    Tool for getting NDC status information from Rxnorm.
    
    Description:
        Retrieve NDC status information for given NDC codes using the RxNAV REST API.
        Returns status details for National Drug Codes.
    
    Input Parameters:
        - ndc (str, required): National Drug Code
        - history (int, optional): Include historical information (0 or 1)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing NDC status information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get NDC status information from Rxnorm."""
        try:
            # 构建URL - ndc在路径中，其他参数作为查询参数
            ndc = params.get("ndc", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/ndcstatus.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for NDC status")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
