"""
Bio.Seq Count Tool - Count occurrences of subsequences in biological sequences.

This tool provides sequence counting functionality using BioPython's Bio.Seq module.
Useful for motif analysis, GC content calculation, and codon frequency analysis.
"""

from typing import Dict, Any
from Bio.Seq import Seq
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqCountTool(Tool):
    """Tool for counting subsequence occurrences in biological sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Count occurrences of a subsequence in a biological sequence.
        
        Args:
            params: Dictionary containing:
                - sequence (str): Input nucleotide or protein sequence
                - subsequence (str): Subsequence to count
                - overlap (bool, optional): Whether to count overlapping matches
                
        Returns:
            Dictionary with count result or error message
        """
        try:
            sequence = params.get('sequence')
            subsequence = params.get('subsequence')
            overlap = params.get('overlap', False)
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            if not subsequence:
                return {"error": "Missing required parameter: subsequence"}
                
            # Clean sequences
            clean_sequence = ''.join(sequence.upper().split())
            clean_subsequence = ''.join(subsequence.upper().split())
            
            if not clean_subsequence:
                return {"error": "Subsequence cannot be empty"}
                
            # Create Seq object and count
            seq_obj = Seq(clean_sequence)
            
            if overlap:
                # Manual counting for overlapping matches
                count = 0
                start = 0
                while True:
                    pos = seq_obj.find(clean_subsequence, start)
                    if pos == -1:
                        break
                    count += 1
                    start = pos + 1
            else:
                # Use Bio.Seq's count method (non-overlapping)
                count = seq_obj.count(clean_subsequence)
            
            return {
                "count": count,
                "sequence_length": len(clean_sequence),
                "subsequence": clean_subsequence,
                "subsequence_length": len(clean_subsequence),
                "overlap_mode": overlap
            }
            
        except Exception as e:
            return {"error": f"Count operation failed: {str(e)}"}
