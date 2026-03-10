"""
外汇日线行情工具
"""
import os
import json
import tushare as ts
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class FxDailyTool(Tool):
    """外汇日线行情工具"""
    
    def __init__(self):
        super().__init__()
        self._name = "外汇日线行情"
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
        """执行外汇日线行情查询
        
        Args:
            context: 执行上下文
            params: 查询参数
                - ts_code: TS代码，可选
                - trade_date: 交易日期（GMT，YYYYMMDD格式），可选
                - start_date: 开始日期（GMT），可选
                - end_date: 结束日期（GMT），可选
                - exchange: 交易商（目前只有FXCM），可选
                
        Returns:
            外汇日线行情数据列表
        """
        try:
            pro = self._get_pro_api()
            if pro is None:
                return {"error": "无法连接到tushare pro api"}
            
            df = pro.fx_daily(**params)
            if df is not None and not df.empty:
                return {"data": df.to_dict('records'), "count": len(df)}
            else:
                return {"data": [], "count": 0}
        except Exception as e:
            return {"error": str(e)}
