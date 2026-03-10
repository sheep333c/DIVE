#!/usr/bin/env python3
"""
ETF复权因子工具
获取ETF复权因子数据，用于计算ETF的前复权和后复权价格
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class EtfAdjTool(Tool):
    """ETF复权因子工具
    
    Retrieves ETF adjustment factors for calculating forward and backward 
    adjusted prices, handling dividend distributions and stock splits.
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
        """Execute ETF adjustment factor data query."""
        try:
            pro = self._get_pro_api()
            df = pro.fund_adj(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
