#!/usr/bin/env python3
"""
资产负债表(专业版)工具
获取上市公司资产负债表数据(专业版)，包括更详细的资产负债项目
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockBalancesheetVipTool(Tool):
    """资产负债表(专业版)工具
    
    Retrieves comprehensive balance sheet data (VIP version) including
    detailed asset, liability and equity items with extended financial positions.
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
        """Execute balance sheet VIP query."""
        try:
            pro = self._get_pro_api()
            df = pro.balancesheet_vip(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
