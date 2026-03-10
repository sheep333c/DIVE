#!/usr/bin/env python3
"""
前十大流通股东工具
获取上市公司前十大流通股东信息，包括股东名称、持股数量、持股比例等
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockTop10FloatHoldersTool(Tool):
    """前十大流通股东工具
    
    Retrieves information about the top 10 float shareholders of listed companies 
    including shareholder names, float shareholdings, and shareholding ratios.
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
        """Execute top 10 float shareholders query."""
        try:
            pro = self._get_pro_api()
            df = pro.top10_floatholders(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
