"""
Clinical Tables API - HUGO基因搜索

提供对HUGO（人类基因组组织）基因命名委员会基因数据的搜索功能。
"""
from __future__ import annotations

import json
import urllib.parse
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class HugoGenesTool(Tool):
    """
    Tool for searching HUGO genes.
    
    Description:
        Search HUGO (Human Genome Organisation) Gene Nomenclature Committee gene data.
        Provides access to official gene symbols, names, and identifiers.
    
    Input Parameters:
        - terms (str, required): Search keywords for gene symbols or names
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
        - Success: JSON array containing HUGO gene data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """
        
    def __init__(self):
        """Initialize the tool with its descriptor."""
        super().__init__()
        
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search HUGO genes."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://clinicaltables.nlm.nih.gov/api/genes/v3/search"
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
