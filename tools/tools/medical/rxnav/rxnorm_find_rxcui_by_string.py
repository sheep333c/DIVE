"""
Tool for finding RxCUI by string in Rxnorm data.

This tool searches for Rxnorm concepts by drug name string.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxnormFindRxcuiByStringTool(Tool):
    """
    Tool for finding RxCUI by string in Rxnorm data.
    
    Description:
        Search for Rxnorm concept unique identifiers (RxCUI) by drug name string using the RxNAV REST API.
        Returns matching RxCUIs for given drug names.
    
    Input Parameters:
        - name (str, required): Drug name to search for
        - sources (str, optional): Source vocabularies to search
        - allsrc (int, optional): Include all sources (0 or 1)
        - search (int, optional): Search type (0=exact, 1=normalized, 2=contains)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing search results and RxCUIs
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find RxCUI by string in Rxnorm data."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API to find RxCUI by string")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
