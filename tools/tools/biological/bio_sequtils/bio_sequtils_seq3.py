"""
Bio.SeqUtils Seq3 Tool - Convert protein sequence from one-letter to three-letter code.

This tool uses BioPython's Bio.SeqUtils.seq3 function to convert
single-letter amino acid codes (like AGF) to three-letter codes (Ala-Gly-Phe),
which is useful for protein visualization and detailed analysis.
"""

from typing import Dict, Any
from Bio.SeqUtils import seq3
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsSeq3Tool(Tool):
    """Tool for converting protein sequences from one-letter to three-letter code."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert protein sequence from one-letter to three-letter amino acid code.
        
        Args:
            params: Dictionary containing:
                - sequence (str): One-letter amino acid sequence
                - custom_map (dict, optional): Custom amino acid mapping
                - undef_code (str, optional): Code for undefined amino acids
                
        Returns:
            Dictionary with converted sequence or error message
        """
        try:
            sequence = params.get('sequence')
            custom_map = params.get('custom_map')
            undef_code = params.get('undef_code', 'Xaa')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
                
            # Build parameters for seq3
            seq3_params = {'seq': sequence}
            if custom_map is not None:
                seq3_params['custom_map'] = custom_map
            if 'undef_code' in params:
                seq3_params['undef_code'] = undef_code
                
            # Convert using Bio.SeqUtils.seq3
            converted_sequence = seq3(**seq3_params)
            
            return {
                "converted_sequence": converted_sequence,
                "original_length": len(sequence),
                "converted_length": len(converted_sequence),
                "conversion_type": "one_letter_to_three_letter"
            }
            
        except Exception as e:
            return {"error": f"Sequence conversion failed: {str(e)}"}
