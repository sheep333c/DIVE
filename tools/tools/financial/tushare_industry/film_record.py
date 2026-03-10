"""
全国电影剧本备案数据工具
"""
import tushare as ts
import os
import json
from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class FilmRecordTool(Tool):
    """全国电影剧本备案数据工具"""
    
    def __init__(self):
        super().__init__()
        self._pro_api = None
        self._name = "全国电影剧本备案数据"
    
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
        """执行全国电影剧本备案数据查询
        
        Args:
            context: 执行上下文
            params: 查询参数
                - ann_date: 公布日期，可选
                - start_date: 开始日期，可选
                - end_date: 结束日期，可选
                
        Returns:
            电影剧本备案数据列表
        """
        try:
            pro = self._get_pro_api()
            df = pro.film_record(**params)
            return df.to_dict('records') if not df.empty else []
        except Exception as e:
            return {"error": str(e)}
