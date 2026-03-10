"""
Tool for retrieving historical stock name change records from Tushare Pro API.

This tool provides access to stock name change history including start/end dates,
announcement dates, and change reasons.
"""

import tushare as ts
from typing import Dict, Any
from ...core.tool import Tool
from ...core.types import ExecutionContext


class StockNameChangeTool(Tool):
    """
    Tool for retrieving stock historical name change records.
    
    Description:
        Retrieve historical stock name change records from Tushare Pro API,
        including name usage periods, announcement dates, and change reasons.
    
    Input Parameters:
        - ts_code (str, optional): Stock code in TS format (e.g., '600848.SH')
        - start_date (str, optional): Start date for announcement date filter (YYYYMMDD)
        - end_date (str, optional): End date for announcement date filter (YYYYMMDD)  
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
        """Execute stock name change query."""
        try:
            # Initialize API and execute query - 直接使用所有参数
            pro = self._get_pro_api()
            df = pro.namechange(**params)
            
            # 直接返回API的原始响应
            return df.to_dict('records') if not df.empty else []
                
        except Exception as e:
            return {"error": str(e)}
