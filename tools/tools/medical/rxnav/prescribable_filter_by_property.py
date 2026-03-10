"""
Tool for filtering prescribable Rxnorm concepts by property values.

This tool returns concepts that match specified property criteria.
"""

import json
from typing import Any, Dict, List
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableFilterByPropertyTool(Tool):
    """
    Tool for filtering prescribable Rxnorm concepts by property values.
    
    Description:
        Filter prescribable Rxnorm concepts to check if they match specified property criteria.
        Uses the RxNAV REST API to validate property values for a given RxCUI.
    
    Input Parameters:
        - rxcui (str, required): Rxnorm Concept Unique Identifier
        - propName (str, required): Property name to filter by (e.g., "AVAILABLE_STRENGTH", "has_tradename")
        - propValues (str, optional): Specific property values to match against
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing the filtered concept information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 构建URL - rxcui在路径中，其他参数作为查询参数
            rxcui = params.get("rxcui", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/Prescribe/rxcui/{rxcui}/filter.json"
            
            # 过滤掉rxcui参数，构建查询参数
            query_params = {k: v for k, v in params.items() if k != "rxcui" and v}
            url = f"{base_url}?{urlencode(query_params)}"
            
            # 记录请求URL（如果需要）
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to: {url}")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应，不做任何业务逻辑处理
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            # HTTP错误时返回错误信息，保持简洁
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            # 其他异常时返回错误信息
            return {"error": str(e)}
