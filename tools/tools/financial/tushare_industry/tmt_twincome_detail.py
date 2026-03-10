"""
台湾电子产业月营收明细工具
"""
import tushare as ts
import os
import json
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TmtTwincomeDetailTool(Tool):
    """台湾电子产业月营收明细工具"""
    
    def __init__(self):
        super().__init__()
        self._pro_api = None
        self._name = "台湾电子产业月营收明细"
        
    
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
        """执行台湾电子产业月营收明细查询
        
        Args:
            context: 执行上下文
            params: 查询参数
                - date: 报告期，可选
                - item: 产品代码，必选
                - start_date: 报告期开始日期，可选
                - end_date: 报告期结束日期，可选
                
        Returns:
            台湾电子产业月营收明细数据列表
        """
        try:
            pro = self._get_pro_api()
            df = pro.tmt_twincomedetail(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
