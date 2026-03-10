"""
Tool for getting class contexts from Rxclass.

This tool retrieves context information for drug classifications.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxclassGetClassContextsTool(Tool):
    """
    Tool for getting class contexts from Rxclass.
    
    Description:
        Retrieve context information for drug classifications using the RxNAV REST API.
        Returns contextual information about how classes are used and related.
    
    Input Parameters:
        - classId (str, required): Drug class identifier
        - relaSource (str, optional): Relationship source
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing class contexts
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get class contexts from Rxclass."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/rxclass/classContext.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for class contexts")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
