"""
Bio.SeqUtils GC Skew Tool - Calculate GC skew along sequence windows.

This tool uses BioPython's Bio.SeqUtils.GC_skew function to calculate
GC skew (G-C)/(G+C) for multiple windows along the sequence, which is
useful for analyzing replication origins and genome structure.
"""

from typing import Dict, Any
from Bio.SeqUtils import GC_skew
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsGcSkewTool(Tool):
    """Tool for calculating GC skew along sequence windows."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate GC skew (G-C)/(G+C) for multiple windows along sequence.
        
        Args:
            params: Dictionary containing:
                - sequence (str): DNA sequence
                - window (int, optional): Window size for analysis (default: 100)
                
        Returns:
            Dictionary with GC skew values or error message
        """
        try:
            sequence = params.get('sequence')
            window = params.get('window', 100)
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Clean sequence
            clean_sequence = ''.join(sequence.upper().split())
            
            # Calculate GC skew using Bio.SeqUtils.GC_skew
            skew_values = GC_skew(clean_sequence, window=window)
            
            return {
                "gc_skew_values": [round(val, 4) for val in skew_values],
                "window_size": window,
                "sequence_length": len(clean_sequence),
                "window_count": len(skew_values)
            }
            
        except Exception as e:
            return {"error": f"GC skew calculation failed: {str(e)}"}
