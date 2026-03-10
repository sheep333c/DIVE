"""
Bio.SeqUtils GC123 Tool - Calculate GC content by codon position.

This tool uses BioPython's Bio.SeqUtils.GC123 function to calculate
G+C content separately for first, second, and third codon positions,
which is important for analyzing codon usage bias and evolutionary patterns.
"""

from typing import Dict, Any
from Bio.SeqUtils import GC123
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsGc123Tool(Tool):
    """Tool for calculating GC content by codon position in coding sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate GC content for each codon position (1st, 2nd, 3rd) and total.
        
        Args:
            params: Dictionary containing:
                - sequence (str): DNA coding sequence (should be multiple of 3)
                
        Returns:
            Dictionary with GC content by position or error message
        """
        try:
            sequence = params.get('sequence')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Clean sequence
            clean_sequence = ''.join(sequence.upper().split())
            
            # Calculate GC content by codon position using Bio.SeqUtils.GC123
            gc_results = GC123(clean_sequence)
            
            return {
                "total_gc": round(gc_results[0], 2),
                "first_position_gc": round(gc_results[1], 2),
                "second_position_gc": round(gc_results[2], 2),
                "third_position_gc": round(gc_results[3], 2),
                "sequence_length": len(clean_sequence),
                "codon_count": len(clean_sequence) // 3
            }
            
        except Exception as e:
            return {"error": f"GC123 calculation failed: {str(e)}"}
