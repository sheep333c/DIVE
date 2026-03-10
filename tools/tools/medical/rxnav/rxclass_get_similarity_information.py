"""
Tool for getting similarity information from Rxclass.

This tool retrieves similarity information for drug classes.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxclassGetSimilarityInformationTool(Tool):
    """
    Tool for getting similarity information from Rxclass.
    
    Description:
        Retrieve similarity information for drug classes using the RxNAV REST API.
        Returns information about class similarities and relationships.
    
    Input Parameters:
        - classId (str, required): Class identifier
        - relaSource (str, optional): Relationship source
        - className (str, optional): Class name for search
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing similarity information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get similarity information from Rxclass."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/rxclass/class/similarInfo.json"
            
            # 直接使用所有非None参数构建查询字符串（保留空字符串）
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for similarity information")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
