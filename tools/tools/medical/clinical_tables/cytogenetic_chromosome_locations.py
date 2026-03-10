"""
Clinical Tables API - 细胞遗传学位置搜索

提供对细胞遗传学位置信息的访问，数据来源于NCBI理想图数据。
"""
from __future__ import annotations

import json
import os
import urllib.parse
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Any, Dict, Optional

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class CytogeneticChromosomeLocationsTool(Tool):
    """
    Tool for searching cytogenetic chromosome locations.
    
    Description:
        Search cytogenetic location information sourced from NCBI ideogram data.
        Supports searching chromosome locations like "1p36.32", "2q21", etc.
    
    Input Parameters:
        - terms (str, required): Search keywords for cytogenetic locations
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
        - Success: JSON array containing cytogenetic location data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    """
        
    def __init__(self):
        """Initialize the tool with its descriptor."""
        super().__init__()
        
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search cytogenetic chromosome locations."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://clinicaltables.nlm.nih.gov/api/cytogenetic_locs/v3/search"
            query_string = urllib.parse.urlencode(params)
            url = f"{base_url}?{query_string}"
            

            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
