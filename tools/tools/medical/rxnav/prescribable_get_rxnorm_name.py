"""
Tool for getting Rxnorm name from Prescribable.

This tool retrieves the Rxnorm name for a given concept.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableGetRxnormNameTool(Tool):
    """
    Tool for getting Rxnorm name from Prescribable.
    
    Description:
        Retrieve the Rxnorm name for a given concept using the RxNAV REST API.
        Returns the official Rxnorm name associated with the specified concept.
    
    Input Parameters:
        - rxcui (str, required): Rxnorm Concept Unique Identifier
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing Rxnorm name information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get Rxnorm name from Prescribable."""
        try:
            # 构建URL - rxcui在路径中
            rxcui = params.get("rxcui", "")
            base_url = f"https://rxnav.nlm.nih.gov/REST/Prescribe/rxcui/{rxcui}.json"
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for Rxnorm name")
            
            with urlopen(base_url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
