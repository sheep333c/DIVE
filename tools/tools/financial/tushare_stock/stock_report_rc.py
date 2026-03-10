#!/usr/bin/env python3
"""
券商盈利预测数据工具
获取券商盈利预测数据，包括EPS预测、营收预测等信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockReportRcTool(Tool):
    """券商盈利预测数据工具
    
    Retrieves broker earnings forecast data including
    EPS forecasts, revenue predictions and analyst estimates.
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
        """Execute broker earnings forecast data query."""
        try:
            pro = self._get_pro_api()
            df = pro.report_rc(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
