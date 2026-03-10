"""
Tool for getting all historical NDCs from Rxnorm.

This tool retrieves all historical National Drug Codes from Rxnorm.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormGetAllHistoricalNdcsTool(Tool):
    """
    Tool for getting all historical NDCs from Rxnorm.
    
    Description:
        Retrieve all historical National Drug Codes from Rxnorm using the RxNAV REST API.
        Returns comprehensive list of NDCs that are no longer active.
    
    Input Parameters:
        - startMonth (str, optional): Start month for historical data (YYYY-MM format)
        - endMonth (str, optional): End month for historical data (YYYY-MM format)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing all historical NDCs
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get all historical NDCs from Rxnorm."""
        try:
            # 构建URL和查询参数
            rxcui = params.get("rxcui", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/allhistoricalndcs.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for all historical NDCs")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
