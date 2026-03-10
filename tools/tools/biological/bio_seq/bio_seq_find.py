"""
Bio.Seq Find Tool - Find positions of subsequences in biological sequences.

This tool provides sequence search functionality using BioPython's Bio.Seq module.
Useful for finding restriction sites, start codons, motifs, and other sequence features.
"""

from typing import Dict, Any, List
from Bio.Seq import Seq
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqFindTool(Tool):
    """Tool for finding subsequence positions in biological sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find positions of a subsequence in a biological sequence.
        
        Args:
            params: Dictionary containing:
                - sequence (str): Input nucleotide or protein sequence
                - subsequence (str): Subsequence to find
                - find_all (bool, optional): Whether to find all occurrences or just first
                - start (int, optional): Start position for search
                - end (int, optional): End position for search
                
        Returns:
            Dictionary with position(s) found or error message
        """
        try:
            sequence = params.get('sequence')
            subsequence = params.get('subsequence')
            find_all = params.get('find_all', False)
            start = params.get('start', 0)
            end = params.get('end')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            if not subsequence:
                return {"error": "Missing required parameter: subsequence"}
                
            # Clean sequences
            clean_sequence = ''.join(sequence.upper().split())
            clean_subsequence = ''.join(subsequence.upper().split())
            
            if not clean_subsequence:
                return {"error": "Subsequence cannot be empty"}
                
            # Validate start/end positions
            seq_length = len(clean_sequence)
            if start < 0:
                start = 0
            if end is None:
                end = seq_length
            elif end > seq_length:
                end = seq_length
                
            if start >= end:
                return {"error": "Invalid start/end positions"}
                
            # Create Seq object
            seq_obj = Seq(clean_sequence)
            
            if find_all:
                # Find all positions
                positions = []
                search_start = start
                while search_start < end:
                    pos = seq_obj.find(clean_subsequence, search_start, end)
                    if pos == -1:
                        break
                    positions.append(pos)
                    search_start = pos + 1
                    
                return {
                    "positions": positions,
                    "count": len(positions),
                    "sequence_length": seq_length,
                    "subsequence": clean_subsequence,
                    "subsequence_length": len(clean_subsequence),
                    "search_range": [start, end],
                    "found": len(positions) > 0
                }
            else:
                # Find first position only
                position = seq_obj.find(clean_subsequence, start, end)
                
                return {
                    "position": position,
                    "sequence_length": seq_length,
                    "subsequence": clean_subsequence,
                    "subsequence_length": len(clean_subsequence),
                    "search_range": [start, end],
                    "found": position != -1
                }
            
        except Exception as e:
            return {"error": f"Find operation failed: {str(e)}"}
