#!/usr/bin/env python3
"""
现金流量表(专业版)工具
获取上市公司现金流量表数据(专业版)，包括更详细的现金流项目
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockCashflowVipTool(Tool):
    """现金流量表(专业版)工具
    
    Retrieves comprehensive cash flow statement data (VIP version) including
    detailed operating, investing and financing cash flow items with extended liquidity metrics.
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
        """Execute cash flow statement VIP query."""
        try:
            pro = self._get_pro_api()
            df = pro.cashflow_vip(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
