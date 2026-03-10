#!/usr/bin/env python3
"""
同花顺涨跌停榜单工具
获取同花顺涨跌停榜单数据，包括涨跌停股票列表等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockLimitListThsTool(Tool):
    """同花顺涨跌停榜单工具
    
    Retrieves THS (Tonghuashun) limit up/down list data including
    limit up/down stock lists and price limit rankings.
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
        """Execute THS limit up/down list query."""
        try:
            pro = self._get_pro_api()
            df = pro.limit_list_ths(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
