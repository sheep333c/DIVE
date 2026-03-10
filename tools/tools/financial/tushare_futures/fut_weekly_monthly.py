#!/usr/bin/env python3
"""期货周月线行情工具"""

import tushare as ts
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext
import json
import os

class FutWeeklyMonthlyTool(Tool):
    """期货周月线行情工具 - 获取期货周线或月线行情数据"""
    
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
        """执行期货周月线行情查询"""
        try:
            pro = self._get_pro_api()
            df = pro.fut_weekly_monthly(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
