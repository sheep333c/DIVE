"""
Clinical Tables API - PharmVar星号等位基因搜索

提供对PharmVar星号等位基因数据的搜索功能，用于药物基因组学研究。
"""
from __future__ import annotations

import json
import urllib.parse
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PharmvarStarAllelesTool(Tool):
    """
    Tool for searching PharmVar star alleles.
    
    Description:
        Search PharmVar star allele nomenclature data for pharmacogenomics research.
        Provides access to standardized allele naming conventions for drug metabolism genes.
    
    Input Parameters:
        - terms (str, required): Search keywords for star alleles or gene names
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
        - Success: JSON array containing PharmVar star allele data
        - Error: {"error": "HTTP error message"} or {"error": "exception message"}
    
    Design Philosophy:
        Complete API pass-through - no internal validation, direct parameter forwarding to API.
    """
        
    def __init__(self):
        """Initialize the tool with its descriptor."""
        super().__init__()
        
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search PharmVar star alleles."""
        try:
            # 构建URL - 直接使用所有参数
            base_url = "https://clinicaltables.nlm.nih.gov/api/star_alleles/v3/search"
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            with urlopen(url) as response:
                # 直接返回API的原始响应
                return json.loads(response.read().decode('utf-8'))
                
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}
