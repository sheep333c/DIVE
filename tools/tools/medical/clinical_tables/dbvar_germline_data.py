"""
Clinical Tables API - dbVar生殖细胞变异数据搜索

提供对dbVar生殖细胞变异数据的搜索功能，支持遗传变异和结构变异查询。
"""
from __future__ import annotations

import json
import urllib.parse
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class DbvarGermlineDataTool(Tool):
    """
    Tool for searching dbVar germline data.
    
    Description:
        Search dbVar germline variation data including structural variants,
        copy number variations, and other genomic alterations for genetics research.
    
    Input Parameters:
        - terms (str, required): Search keywords for variant identifiers or descriptions
        - maxList (int, optional): Maximum number of items to return (1-500)
        - count (int, optional): Number of items per page (1-500)
        - offset (int, optional): Starting offset (>=0)
        - q (str, optional): Query parameter
        - df (str, optional): Display fields
        - sf (str, optional): Search fields
        - cf (str, optional): Count fields
        - ef (str, optional): Extra fields
    
    Output Format:
        Returns the raw API response directly without modification.
        - Success: JSON array containing dbVar germline variation data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """
        
    def __init__(self):
        """Initialize the tool with its descriptor."""
        super().__init__()
        
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search dbVar germline data."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://clinicaltables.nlm.nih.gov/api/dbvar/v3/search"
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
