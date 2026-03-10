#!/usr/bin/env python3
"""
业绩预告工具
获取上市公司业绩预告数据，包括预告类型、预计净利润等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockForecastTool(Tool):
    """业绩预告工具
    
    Retrieves earnings forecast data for listed companies including forecast types,
    estimated net profit and other preliminary financial performance indicators.
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
        """Execute earnings forecast query."""
        try:
            pro = self._get_pro_api()
            if pro is None:
                return {"error": "无法连接到tushare pro api"}
            
            df = pro.forecast(**params)
            
            if df is not None and not df.empty:
                return {"data": df.to_dict('records'), "count": len(df)}
            else:
                return {"data": [], "count": 0}
        except Exception as e:
            return {"error": str(e)}
