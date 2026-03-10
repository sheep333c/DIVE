#!/usr/bin/env python3
"""
股票利润表工具
获取上市公司财务利润表数据，包括营业收入、净利润、每股收益等关键财务指标
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

import tushare as ts

from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class StockIncomeTool(Tool):
    """股票利润表工具
    
    Retrieves income statement data for listed companies including revenue, net profit, 
    earnings per share, and other key financial metrics from Tushare Pro API.
    
    This tool provides access to comprehensive profit and loss statement data for Chinese listed companies,
    including operating revenue, total costs, net profit, basic and diluted EPS, and various income components.
    The data can be filtered by stock code, reporting period, announcement date, and company type.
    
    Input Parameters:
        - ts_code (str, required): Stock code in TS format (e.g., '000001.SZ')
        - ann_date (str, optional): Announcement date in YYYYMMDD format
        - f_ann_date (str, optional): Actual announcement date in YYYYMMDD format
        - start_date (str, optional): Start date for announcement date filter in YYYYMMDD format
        - end_date (str, optional): End date for announcement date filter in YYYYMMDD format
        - period (str, optional): Reporting period (e.g., '20231231' for annual report, '20230930' for Q3)
        - report_type (str, optional): Report type (see documentation for codes)
        - comp_type (str, optional): Company type (1=General, 2=Bank, 3=Insurance, 4=Securities)
    
    Output Format:
        Returns structured data with income statement information.
        - Success: List of records with financial metrics
        - Error: {"error": "error message"}
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
        """Execute income statement data query."""
        try:
            # Initialize API and execute query - 直接使用所有参数
            pro = self._get_pro_api()
            df = pro.income(**params)
            
            # 直接返回API的原始响应
            return df.to_dict('records') if not df.empty else []
                
        except Exception as e:
            return {"error": str(e)}
