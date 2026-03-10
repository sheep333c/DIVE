"""
Bio.SeqUtils Six Frame Tool - Perform six-frame translation of DNA sequences.

This tool uses BioPython's Bio.SeqUtils.six_frame_translations function to
translate DNA sequences in all six reading frames (3 forward + 3 reverse),
which is useful for gene finding and ORF analysis.
"""

from typing import Dict, Any
from Bio.SeqUtils import six_frame_translations
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsSixFrameTool(Tool):
    """Tool for six-frame translation of DNA sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform six-frame translation of DNA sequence.
        
        Args:
            params: Dictionary containing:
                - sequence (str): DNA sequence
                - genetic_code (int, optional): Genetic code table to use
                
        Returns:
            Dictionary with six-frame translation results or error message
        """
        try:
            sequence = params.get('sequence')
            genetic_code = params.get('genetic_code', 1)
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Clean sequence
            clean_sequence = ''.join(sequence.upper().split())
            
            # Build parameters for six_frame_translations
            six_frame_params = {'seq': clean_sequence}
            if 'genetic_code' in params:
                six_frame_params['genetic_code'] = genetic_code
                
            # Get six-frame translation using Bio.SeqUtils.six_frame_translations
            translation_result = six_frame_translations(**six_frame_params)
            
            return {
                "translation_result": translation_result,
                "sequence_length": len(clean_sequence),
                "genetic_code_used": genetic_code
            }
            
        except Exception as e:
            return {"error": f"Six-frame translation failed: {str(e)}"}
