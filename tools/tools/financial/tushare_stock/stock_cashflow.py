#!/usr/bin/env python3
"""
股票现金流量表工具
获取上市公司现金流量表数据，包括经营、投资、筹资活动现金流等关键财务指标
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockCashFlowTool(Tool):
    """股票现金流量表工具
    
    Retrieves cash flow statement data for listed companies including operating, 
    investing, and financing cash flows from Tushare Pro API.
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
        """Execute cash flow statement data query."""
        try:
            pro = self._get_pro_api()
            df = pro.cashflow(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
