"""
各交易所交易日历工具
"""
import os
import json
import tushare as ts
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TradeCalTool(Tool):
    """各交易所交易日历工具"""
    
    def __init__(self):
        super().__init__()
        self._name = "各交易所交易日历"
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
        """执行各交易所交易日历查询
        
        Args:
            context: 执行上下文
            params: 查询参数
                - exchange: 交易所代码，可选（SSE上交所,SZSE深交所,CFFEX中金所,SHFE上期所,CZCE郑商所,DCE大商所,INE上能源）
                - start_date: 开始日期，可选（格式：YYYYMMDD）
                - end_date: 结束日期，可选
                - is_open: 是否交易，可选（'0'休市 '1'交易）
                
        Returns:
            各交易所交易日历数据列表
        """
        pro = self._get_pro_api()
        df = pro.trade_cal(**params)
        return df.to_dict('records') if not df.empty else []
