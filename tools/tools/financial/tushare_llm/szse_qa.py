"""
深证易互动问答工具
"""
import os
import json
from typing import Dict, Any
import tushare as ts
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class SzseQaTool(Tool):
    """深证易互动问答工具"""
    
    def __init__(self):
        super().__init__()
        self._pro_api = None
        self._name = "深证易互动问答"    
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
        """执行深证易互动问答查询
        
        Args:
            context: 执行上下文
            params: 查询参数
                - ts_code: 股票代码，可选
                - trade_date: 交易日期，可选（格式YYYYMMDD）
                - start_date: 开始日期，可选
                - end_date: 结束日期，可选
                - pub_date: 发布开始日期，可选
                - pub_end_date: 发布结束日期，可选
                
        Returns:
            深证易互动问答数据列表
        """
        pro = self._get_pro_api()
        df = pro.irm_qa_sz(**params)
        return df.to_dict('records') if not df.empty else []
