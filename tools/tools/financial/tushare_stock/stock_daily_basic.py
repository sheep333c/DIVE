#!/usr/bin/env python3
"""
每日行情指标工具
获取股票每日重要的基本面指标，包括市值、PE、PB、总股本、流通股本等
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockDailyBasicTool(Tool):
    """每日行情指标工具
    
    Retrieves daily basic indicators for stocks including market capitalization, 
    PE ratio, PB ratio, total shares, float shares and other fundamental metrics.
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
        """Execute daily basic indicators query."""
        try:
            pro = self._get_pro_api()
            df = pro.daily_basic(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
