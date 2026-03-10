#!/usr/bin/env python3
"""
股票基础列表工具
获取股票基础信息数据，包括股票代码、名称、上市日期、退市日期等
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

import tushare as ts

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockBasicTool(Tool):
    """股票基础列表工具
    
    Retrieves basic stock information including stock code, name, listing date, delisting date, etc.
    from Tushare Pro API.
    
    This tool provides access to comprehensive basic information of stocks listed on Chinese exchanges,
    including stock codes, names, listing dates, markets, industries, and other fundamental data.
    
    Input Parameters:
        - ts_code (str, optional): TS stock code (e.g., '000001.SZ')
        - name (str, optional): Stock name
        - market (str, optional): Market category (主板/创业板/科创板/CDR/北交所)
        - list_status (str, optional): Listing status: L=Listed, D=Delisted, P=Suspended, default=L
        - exchange (str, optional): Exchange: SSE=Shanghai, SZSE=Shenzhen, BSE=Beijing
        - is_hs (str, optional): Stock connect eligible: N=No, H=Shanghai-HK, S=Shenzhen-HK
        - fields (str, optional): Comma-separated list of fields to return
    
    Output Format:
        Returns structured data with query results.
        - Success: {"success": true, "data": [...], "total_records": N}
        - Error: {"success": false, "error": "error message", "data": []}
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
        """Execute stock basic info query."""
        try:
            # Initialize API and execute query - 直接使用所有参数
            pro = self._get_pro_api()
            df = pro.stock_basic(**params)
            
            # 直接返回API的原始响应
            return df.to_dict('records') if not df.empty else []
                
        except Exception as e:
            return {"error": str(e)}
