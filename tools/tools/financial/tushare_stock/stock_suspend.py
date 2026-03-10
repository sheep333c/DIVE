#!/usr/bin/env python3
"""
股票停复牌工具
获取股票停复牌信息，包括停牌日期、复牌日期、停牌类型和停牌原因等
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockSuspendTool(Tool):
    """股票停复牌工具
    
    Retrieves stock suspension and resumption information including suspension dates, 
    resumption dates, suspension types and reasons from Tushare Pro API.
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
        """Execute stock suspension data query."""
        try:
            pro = self._get_pro_api()
            df = pro.suspend_d(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
