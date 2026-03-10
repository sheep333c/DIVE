"""
Bio.SeqUtils GC Content Tool - Calculate GC content in biological sequences.

This tool uses BioPython's Bio.SeqUtils.gc_fraction function to calculate
the G+C percentage in DNA/RNA sequences, which is important for various
biological analyses including primer design and genome characterization.
"""

from typing import Dict, Any
from Bio.SeqUtils import gc_fraction
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsGcContentTool(Tool):
    """Tool for calculating GC content in biological sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate GC content percentage in a DNA/RNA sequence.
        
        Args:
            params: Dictionary containing:
                - sequence (str): DNA or RNA sequence
                - ambiguous (str, optional): How to handle ambiguous nucleotides
                
        Returns:
            Dictionary with GC content results or error message
        """
        try:
            sequence = params.get('sequence')
            ambiguous = params.get('ambiguous', 'ignore')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Clean sequence
            clean_sequence = ''.join(sequence.upper().split())
            
            # Build parameters for gc_fraction
            gc_params = {'seq': clean_sequence}
            if 'ambiguous' in params:
                gc_params['ambiguous'] = ambiguous
                
            # Calculate GC content using Bio.SeqUtils.gc_fraction
            gc_fraction_result = gc_fraction(**gc_params)
            gc_percentage = gc_fraction_result * 100
            
            return {
                "gc_content": round(gc_percentage, 2),
                "gc_fraction": round(gc_fraction_result, 4),
                "sequence_length": len(clean_sequence)
            }
            
        except Exception as e:
            return {"error": f"GC content calculation failed: {str(e)}"}
