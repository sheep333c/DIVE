"""
ExPASy PROSITE tool for retrieving protein domain and family information.

This tool retrieves PROSITE entries from ExPASy database.
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class ExPASyPrositeTools(Tool):
    """
    Tool for retrieving PROSITE entries from ExPASy.
    
    Uses Bio.ExPASy to get PROSITE protein domain and family information
    for specific PROSITE identifiers.
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve PROSITE entry from ExPASy.
        
        Args:
            context: Execution context
            params: Dictionary containing:
                - prosite_id (str): PROSITE identifier (e.g., "PS00001")
                - format (str, optional): Output format ("html" or "raw") (default: "raw")
        
        Returns:
            Dict containing PROSITE entry data
        """
        try:
            from Bio import ExPASy
            
            # Extract parameters
            prosite_id = params.get('prosite_id', '')
            output_format = params.get('format', 'raw')
            
            # Validate inputs
            if not prosite_id:
                return {"error": "PROSITE ID parameter is required"}
            
            if output_format not in ['html', 'raw']:
                return {"error": "Format must be 'html' or 'raw'"}
            
            # Validate PROSITE ID format (should start with PS)
            if not prosite_id.upper().startswith('PS'):
                return {"error": "PROSITE ID should start with 'PS' (e.g., PS00001)"}
            
            # Perform request with retry mechanism
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    if output_format == 'html':
                        # Get HTML format
                        with ExPASy.get_prosite_entry(prosite_id) as handle:
                            data = handle.read()
                            if isinstance(data, bytes):
                                data = data.decode('utf-8')
                    else:
                        # Get raw format
                        with ExPASy.get_prosite_raw(prosite_id) as handle:
                            data = handle.read()
                            if isinstance(data, bytes):
                                data = data.decode('utf-8')
                    
                    # Check if entry exists
                    if 'There is currently no PROSITE entry' in data:
                        return {
                            "error": f"No PROSITE entry found for ID: {prosite_id}",
                            "prosite_id": prosite_id,
                            "format": output_format
                        }
                    
                    return data
                    
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
                "error": f"ExPASy PROSITE request failed: {error_msg}",
                "prosite_id": params.get('prosite_id', ''),
                "format": params.get('format', 'raw')
            }
