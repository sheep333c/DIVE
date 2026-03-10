"""
Bio.SeqUtils Seq1 Tool - Convert protein sequence from three-letter to one-letter code.

This tool uses BioPython's Bio.SeqUtils.seq1 function to convert
three-letter amino acid codes (like Ala-Gly-Phe) to single-letter codes (AGF),
which is useful for protein sequence analysis and database searching.
"""

from typing import Dict, Any
from Bio.SeqUtils import seq1
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsSeq1Tool(Tool):
    """Tool for converting protein sequences from three-letter to one-letter code."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert protein sequence from three-letter to one-letter amino acid code.
        
        Args:
            params: Dictionary containing:
                - sequence (str): Three-letter amino acid sequence
                - custom_map (dict, optional): Custom amino acid mapping
                - undef_code (str, optional): Code for undefined amino acids
                
        Returns:
            Dictionary with converted sequence or error message
        """
        try:
            sequence = params.get('sequence')
            custom_map = params.get('custom_map')
            undef_code = params.get('undef_code', 'X')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Build parameters for seq1
            seq1_params = {'seq': sequence}
            if custom_map is not None:
                seq1_params['custom_map'] = custom_map
            if 'undef_code' in params:
                seq1_params['undef_code'] = undef_code
                
            # Convert using Bio.SeqUtils.seq1
            converted_sequence = seq1(**seq1_params)
            
            return {
                "converted_sequence": converted_sequence,
                "original_length": len(sequence),
                "converted_length": len(converted_sequence),
                "conversion_type": "three_letter_to_one_letter"
            }
            
        except Exception as e:
            return {"error": f"Sequence conversion failed: {str(e)}"}
