"""
ExPASy PROSITE Raw tool for retrieving raw PROSITE records.

This tool retrieves raw PROSITE records from ExPASy database.
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class ExPASyPrositeRawTool(Tool):
    """
    Tool for retrieving raw PROSITE records from ExPASy.
    
    Uses Bio.ExPASy to get raw PROSITE protein patterns and profiles
    in plain text format.
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve raw PROSITE record from ExPASy.
        
        Args:
            context: Execution context
            params: Dictionary containing:
                - prosite_id (str): PROSITE identifier (e.g., "PS00001")
        
        Returns:
            Dict containing raw PROSITE record data
        """
        try:
            from Bio import ExPASy
            
            # Extract parameters
            prosite_id = params.get('prosite_id', '')
            
            # Validate inputs
            if not prosite_id:
                return {"error": "PROSITE ID parameter is required"}
            
            # Validate PROSITE ID format (should start with PS)
            if not prosite_id.upper().startswith('PS'):
                return {"error": "PROSITE ID should start with 'PS' (e.g., PS00001)"}
            
            # Perform request with retry mechanism
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # Get raw PROSITE record
                    with ExPASy.get_prosite_raw(prosite_id) as handle:
                        data = handle.read()
                        if isinstance(data, bytes):
                            data = data.decode('utf-8')
                    
                    # Check if entry exists
                    if not data or len(data) < 10:
                        return {
                            "error": f"No PROSITE entry found for ID: {prosite_id}",
                            "prosite_id": prosite_id
                        }
                    
                    # Parse some basic info from the raw data
                    lines = data.split('\n')
                    entry_info = {}
                    for line in lines:
                        if line.startswith('ID   '):
                            entry_info['entry_id'] = line[5:].strip()
                        elif line.startswith('AC   '):
                            entry_info['accession'] = line[5:].strip()
                        elif line.startswith('DE   '):
                            entry_info['description'] = line[5:].strip()
                        elif line.startswith('PA   '):
                            entry_info['pattern'] = line[5:].strip()
                    
                    return {
                        "prosite_id": prosite_id,
                        "data": data,
                        "data_length": len(data),
                        "format": "prosite_raw",
                        "entry_info": entry_info,
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
                "error": f"ExPASy PROSITE raw request failed: {error_msg}",
                "prosite_id": params.get('prosite_id', '')
            }
