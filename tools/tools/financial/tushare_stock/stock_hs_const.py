#!/usr/bin/env python3
"""
沪深港通股票列表工具
获取沪深港通标的股票列表，包括沪股通、深股通标的
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockHsConstTool(Tool):
    """沪深港通股票列表工具
    
    Retrieves Shanghai-Hong Kong Stock Connect and Shenzhen-Hong Kong Stock Connect
    constituent stocks including eligible stocks for northbound and southbound trading.
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
        """Execute Shanghai-Shenzhen-Hong Kong Stock Connect constituents query."""
        try:
            pro = self._get_pro_api()
            df = pro.stock_hsgt(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
