#!/usr/bin/env python3
"""
概念股明细工具
获取概念股明细列表，包括每个概念下的具体股票信息
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockConceptDetailTool(Tool):
    """概念股明细工具
    
    Retrieves detailed list of concept stocks showing specific
    stocks under each concept category with detailed information.
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
        """Execute concept stock detail query."""
        try:
            pro = self._get_pro_api()
            df = pro.concept_detail(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
