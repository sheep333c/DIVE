#!/usr/bin/env python3
"""
股票财务指标工具
获取上市公司财务指标数据，包括ROE、ROA、净利率、资产负债率等关键分析指标
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockFinaIndicatorTool(Tool):
    """股票财务指标工具
    
    Retrieves financial indicator data for listed companies including ROE, ROA, 
    profit margins, debt ratios and other key analytical metrics from Tushare Pro API.
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
        """Execute financial indicator data query."""
        try:
            pro = self._get_pro_api()
            df = pro.fina_indicator(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
