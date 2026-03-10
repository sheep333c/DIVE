"""
Tool for getting drugs for a prescribable drug concept.

This tool retrieves drug information for a given RxCUI.
"""

import json
from typing import Any, Dict
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PrescribableGetDrugsTool(Tool):
    """
    Tool for getting drugs for a prescribable drug concept.
    
    Description:
        Retrieve drug products associated with a specified name using the RxNAV Prescribable API.
        Returns related drug concepts and information for ingredients, brands, dose forms, and drug components.
    
    Input Parameters:
        - name (str, required): Name of ingredient, brand, clinical dose form, branded dose form, clinical drug component, or branded drug component
        - expand (str, optional): Additional result fields to retrieve ("psn" for Prescribable Name)
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON object containing drug information
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get drugs for a prescribable drug concept."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://rxnav.nlm.nih.gov/REST/Prescribe/drugs.json"
            url = f"{base_url}?{urlencode(params)}"
            
            if hasattr(context, 'logger') and context.logger:
                context.logger.info(f"Making request to RxNAV API for drugs")
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
