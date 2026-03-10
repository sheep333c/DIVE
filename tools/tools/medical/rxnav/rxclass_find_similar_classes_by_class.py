"""
Tool for finding similar classes by class from Rxclass.

This tool finds drug classes similar to a specified class.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxclassFindSimilarClassesByClassTool(Tool):
    """
    Tool for finding similar classes by class from Rxclass.
    
    Description:
        Find drug classes similar to a specified class using the RxNAV REST API.
        Returns classes that are similar to the provided class.
    
    Input Parameters:
        - classId (str, required): Class identifier
        - relaSource (str, optional): Relationship source
        - rela (str, optional): Relationship type
        - classType (str, optional): Type of classification
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing similar classes information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find similar classes by class from Rxclass."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/rxclass/class/similar.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for similar classes by class")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
