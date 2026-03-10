#!/usr/bin/env python3
"""
涨跌停数据明细工具
获取详细的涨跌停数据，包括涨跌停原因、封单量、炸板次数等详细信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockLimitListDTool(Tool):
    """涨跌停数据明细工具
    
    Retrieves detailed limit up/down data including reasons for limits,
    sealed order volume, board breaking times and other detailed information.
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
        """Execute detailed limit list query."""
        try:
            pro = self._get_pro_api()
            df = pro.limit_list_d(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
