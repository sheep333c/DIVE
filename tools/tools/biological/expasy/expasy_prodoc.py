"""
ExPASy PRODOC tool for retrieving protein documentation.

This tool retrieves PRODOC entries from ExPASy database.
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class ExPASyProdocTool(Tool):
    """
    Tool for retrieving PRODOC entries from ExPASy.
    
    Uses Bio.ExPASy to get PRODOC protein documentation and annotation
    for specific PRODOC identifiers.
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve PRODOC entry from ExPASy.
        
        Args:
            context: Execution context
            params: Dictionary containing:
                - prodoc_id (str): PRODOC identifier (e.g., "PDOC00001")
        
        Returns:
            Dict containing PRODOC entry data
        """
        try:
            from Bio import ExPASy
            
            # Extract parameters
            prodoc_id = params.get('prodoc_id', '')
            
            # Validate inputs
            if not prodoc_id:
                return {"error": "PRODOC ID parameter is required"}
            
            # Validate PRODOC ID format (should start with PDOC)
            if not prodoc_id.upper().startswith('PDOC'):
                return {"error": "PRODOC ID should start with 'PDOC' (e.g., PDOC00001)"}
            
            # Perform request with retry mechanism
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # Get PRODOC entry in HTML format
                    with ExPASy.get_prodoc_entry(prodoc_id) as handle:
                        data = handle.read()
                        if isinstance(data, bytes):
                            data = data.decode('utf-8')
                    
                    # Check if entry exists
                    if 'There is currently no PROSITE entry' in data or 'not found' in data.lower():
                        return {
                            "error": f"No PRODOC entry found for ID: {prodoc_id}",
                            "prodoc_id": prodoc_id
                        }
                    
                    return {
                        "prodoc_id": prodoc_id,
                        "data": data,
                        "data_length": len(data),
                        "format": "html",
                        "success": True
                    }
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        if "timeout" in str(retry_e).lower() or "URLError" in str(retry_e):
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            error_msg = str(e)
            return {
                "error": f"ExPASy PRODOC request failed: {error_msg}",
                "prodoc_id": params.get('prodoc_id', '')
            }
