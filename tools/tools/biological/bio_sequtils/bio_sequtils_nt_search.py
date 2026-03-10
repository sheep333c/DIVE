"""
Bio.SeqUtils NT Search Tool - Search for DNA subsequences with position information.

This tool uses BioPython's Bio.SeqUtils.nt_search function to search
for DNA subsequences and return detailed position information,
which is useful for finding specific motifs, restriction sites, or regulatory elements.
"""

from typing import Dict, Any
from Bio.SeqUtils import nt_search
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqUtilsNtSearchTool(Tool):
    """Tool for searching DNA subsequences with position information."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for DNA subsequence and return position information.
        
        Args:
            params: Dictionary containing:
                - sequence (str): DNA sequence to search in
                - subsequence (str): DNA subsequence to find
                
        Returns:
            Dictionary with search results or error message
        """
        try:
            sequence = params.get('sequence')
            subsequence = params.get('subsequence')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            if not subsequence:
                return {"error": "Missing required parameter: subsequence"}
                
            # Clean sequences
            clean_sequence = ''.join(sequence.upper().split())
            clean_subsequence = ''.join(subsequence.upper().split())
            
            # Search using Bio.SeqUtils.nt_search
            search_result = nt_search(clean_sequence, clean_subsequence)
            
            return {
                "search_result": search_result,
                "sequence_length": len(clean_sequence),
                "subsequence_length": len(clean_subsequence),
                "subsequence_searched": clean_subsequence
            }
            
        except Exception as e:
            return {"error": f"NT search failed: {str(e)}"}
