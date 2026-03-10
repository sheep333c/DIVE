#!/usr/bin/env python3
"""
券商盈利预测数据工具
获取券商盈利预测数据，包括分析师预测的EPS、营收等数据
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockBrokerForecastTool(Tool):
    """券商盈利预测数据工具
    
    Retrieves broker earnings forecast data including analyst predictions
    for EPS, revenue and other financial performance indicators.
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
        """Execute broker forecast query."""
        try:
            pro = self._get_pro_api()
            if pro is None:
                return {"error": "无法连接到tushare pro api"}
            
            # 根据Tushare文档，券商盈利预测数据使用 report_rc 接口
            df = pro.report_rc(**params)
            
            if df is not None and not df.empty:
                return {"data": df.to_dict('records'), "count": len(df)}
            else:
                return {"data": [], "count": 0}
        except Exception as e:
            return {"error": str(e)}
