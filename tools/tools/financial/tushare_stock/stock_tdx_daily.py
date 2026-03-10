#!/usr/bin/env python3
"""
通达信板块行情工具
获取通达信板块行情数据，包括板块涨跌幅、成交量、成交额等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockTdxDailyTool(Tool):
    """通达信板块行情工具
    
    Retrieves TDX (Tongdaxin) sector daily market data including
    sector price changes, trading volume, turnover and other sector performance metrics.
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
        """Execute TDX sector daily data query."""
        try:
            pro = self._get_pro_api()
            df = pro.tdx_daily(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
