#!/usr/bin/env python3
"""
股票日线行情工具
获取A股日线行情数据，包括开盘价、最高价、最低价、收盘价、成交量等
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

import tushare as ts

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockDailyTool(Tool):
    """股票日线行情工具
    
    Retrieves daily stock market data including OHLC (Open, High, Low, Close), 
    volume, and amount from Tushare Pro API.
    
    This tool provides access to historical and current daily trading data for Chinese A-shares,
    including price movements, trading volumes, and other market indicators. Data is available
    for individual stocks or multiple stocks simultaneously.
    
    Input Parameters:
        - ts_code (str, optional): Stock code(s) in TS format, supports multiple codes separated by comma
        - trade_date (str, optional): Trading date in YYYYMMDD format
        - start_date (str, optional): Start date in YYYYMMDD format
        - end_date (str, optional): End date in YYYYMMDD format
    
    Output Format:
        Returns structured data with daily trading information.
        - Success: List of records with ts_code, trade_date, open, high, low, close, volume, etc.
        - Error: {"error": "error message"}
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
        """Execute daily stock data query."""
        try:
            # Initialize API and execute query - 直接使用所有参数
            pro = self._get_pro_api()
            df = pro.daily(**params)
            
            # 直接返回API的原始响应
            return df.to_dict('records') if not df.empty else []
                
        except Exception as e:
            return {"error": str(e)}
