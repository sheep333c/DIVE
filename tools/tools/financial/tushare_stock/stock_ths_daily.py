#!/usr/bin/env python3
"""
同花顺概念和行业指数行情工具
获取同花顺概念和行业指数行情数据，包括指数涨跌幅、成交量等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockThsDailyTool(Tool):
    """同花顺概念和行业指数行情工具
    
    Retrieves THS (Tonghuashun) concept and industry index market data including
    index price changes, trading volumes and sector performance analytics.
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
        """Execute THS concept and industry index data query."""
        try:
            pro = self._get_pro_api()
            df = pro.ths_daily(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
