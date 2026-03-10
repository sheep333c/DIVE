#!/usr/bin/env python3
"""
沪深股通持股明细工具
获取沪深股通持股明细数据，包括港资持股数量、比例等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockHkHoldTool(Tool):
    """沪深股通持股明细工具
    
    Retrieves Shanghai-Shenzhen-Hong Kong Stock Connect holding details including
    Hong Kong capital shareholding quantities, percentages and detailed position information.
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
        """Execute HK Stock Connect holding details query."""
        try:
            pro = self._get_pro_api()
            df = pro.hk_hold(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
