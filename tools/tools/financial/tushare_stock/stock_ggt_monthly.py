#!/usr/bin/env python3
"""
港股通每月成交统计工具
获取港股通每月成交统计数据，包括月度成交金额、成交量等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockGgtMonthlyTool(Tool):
    """港股通每月成交统计工具
    
    Retrieves Hong Kong Stock Connect monthly trading statistics including
    monthly trading amounts, volumes and cross-border trading trends.
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
        """Execute HK Stock Connect monthly trading statistics query."""
        try:
            pro = self._get_pro_api()
            df = pro.ggt_monthly(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
