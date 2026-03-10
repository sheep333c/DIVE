"""
Tool for getting multi-ingredient brand drug concepts.

This tool retrieves multi-ingredient brand information for prescribable concepts.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableGetMultiIngredBrandTool(Tool):
    """
    Tool for getting multi-ingredient brand drug concepts.
    
    Description:
        Retrieve multi-ingredient brand information for prescribable concepts using the RxNAV REST API.
        Returns brand names that contain multiple active ingredients.
    
    Input Parameters:
        - ingredientIds (str, required): Comma-separated list of ingredient RxCUIs
        - sources (str, optional): Source vocabularies to search
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing multi-ingredient brand information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get multi-ingredient brand drug concepts."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/Prescribe/brands.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            if query_params:
                # RxNAV API期望加号不被编码，所以先编码再替换%2B为+
                encoded_query = urlencode(query_params)
                encoded_query = encoded_query.replace('%2B', '+')
                url = f"{base_url}?{encoded_query}"
            else:
                url = base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for multi-ingredient brands")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
