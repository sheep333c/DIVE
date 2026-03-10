#!/usr/bin/env python3
"""
股票开盘集合竞价数据工具
获取股票开盘集合竞价数据，包括集合竞价阶段的买卖盘、价格等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockAuctionOpenTool(Tool):
    """股票开盘集合竞价数据工具
    
    Retrieves stock opening auction data including bids, asks, prices
    and other information during the opening call auction period.
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
        """Execute opening auction data query."""
        try:
            pro = self._get_pro_api()
            if pro is None:
                return {"error": "无法连接到tushare pro api"}
            
            # 根据Tushare文档，开盘集合竞价使用 stk_auction_o 接口
            df = pro.stk_auction_o(**params)
            
            if df is not None and not df.empty:
                return {"data": df.to_dict('records'), "count": len(df)}
            else:
                return {"data": [], "count": 0}
        except Exception as e:
            return {"error": str(e)}
