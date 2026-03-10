"""
Tool for finding similar classes by drug list from Rxclass.

This tool finds similar drug classes based on a list of drugs.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class RxclassFindSimilarClassesByDrugListTool(Tool):
    """
    Tool for finding similar classes by drug list from Rxclass.
    
    Description:
        Find similar drug classes based on a list of drugs using the RxNAV REST API.
        Returns classes that are similar to those containing the provided drugs.
    
    Input Parameters:
        - rxcuis (str, required): Space-separated list of RxCUIs (e.g., '161 1191')
        - relaSource (str, optional): Relationship source
        - rela (str, optional): Relationship type
        - scoreType (str, optional): Ranking type (0=equivalence, 1=includes, 2=included-in)
        - top (str, optional): Number of results (1-100)
        - equivalenceThreshold (str, optional): Minimum equivalence score (0.0-1.0)
        - inclusionThreshold (str, optional): Minimum inclusion score (0.0-1.0)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing similar classes information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find similar classes by drug list from Rxclass."""
        try:
            # 构建URL和查询参数
            base_url = "https://rxnav.nlm.nih.gov/REST/rxclass/class/similarByRxcuis.json"
            
            # 直接使用所有参数构建查询字符串
            query_params = {k: v for k, v in params.items() if v is not None}
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for similar classes by drug list")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
