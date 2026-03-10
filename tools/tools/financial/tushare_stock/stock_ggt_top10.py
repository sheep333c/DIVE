#!/usr/bin/env python3
"""
港股通十大成交股工具
获取港股通十大成交股数据，包括每日港股通最活跃的股票
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockGgtTop10Tool(Tool):
    """港股通十大成交股工具
    
    Retrieves top 10 most traded stocks via HK Stock Connect including
    daily most active securities and trading activity rankings.
    """
    
    def __init__(self):
        super().__init__()
        self._pro_api = None
    
    def _get_pro_api(self):
        """Initialize Tushare Pro API client."""
        if self._pro_api is None:
            # Read token from environment variable
            token = os.getenv("TUSHARE_TOKEN") or os.getenv("TUSHARE_API_KEY")
            if not token:
                raise ValueError(
                    "Tushare token not found. Please set TUSHARE_TOKEN or TUSHARE_API_KEY "
                    "environment variable with your Tushare Pro token."
                )
            ts.set_token(token)
            self._pro_api = ts.pro_api()
        return self._pro_api
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """Execute HK Stock Connect top 10 query."""
        try:
            pro = self._get_pro_api()
            df = pro.ggt_top10(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
