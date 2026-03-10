"""
Tool for getting relationship source version from Rxclass.

This tool retrieves version information for relationship sources.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxclassGetRelaSourceVersionTool(Tool):
    """
    Tool for getting relationship source version from Rxclass.
    
    Description:
        Retrieve version information for relationship sources using the RxNAV REST API.
        Returns source version details for drug class relationships.
    
    Input Parameters:
        - rela (str, optional): Relationship type
        - source (str, optional): Source vocabulary
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing source version information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get relationship source version from Rxclass."""
        try:
            # 构建URL - relaSource在路径中
            rela_source = params.get("relaSource", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/rxclass/version/{rela_source}.json"
            
            # 过滤掉relaSource参数，其他参数作为查询参数
            query_params = {k: v for k, v in params.items() if k != "relaSource" and v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for relationship source version")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
