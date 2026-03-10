#!/usr/bin/env python3
"""
个股资金流向工具(同花顺版)
获取个股资金流向数据(同花顺数据源)，包括主力资金净流入等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockMoneyflowThsTool(Tool):
    """个股资金流向工具(同花顺版)
    
    Retrieves individual stock capital flow data from THS (Tonghuashun) source
    including main capital net inflow and other fund flow indicators.
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
        """Execute stock money flow query (THS version)."""
        try:
            pro = self._get_pro_api()
            df = pro.moneyflow_ths(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
