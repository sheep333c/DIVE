"""
Simple local pairwise sequence alignment tool using Bio.Align.PairwiseAligner.

This tool performs local pairwise sequence alignment with default parameters.
"""

from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class Pairwise2LocalXXTool(Tool):
    """
    Tool for performing simple local pairwise sequence alignment.
    
    Uses Bio.Align.PairwiseAligner for local alignment with default parameters
    (match=1, mismatch=0, no gap penalties).
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform simple local pairwise sequence alignment.
        
        Args:
            context: Execution context
            params: Dictionary containing:
                - sequence_a (str): First sequence to align
                - sequence_b (str): Second sequence to align
                - score_only (bool, optional): Return only the best score (default: False)
                - one_alignment_only (bool, optional): Return only one alignment (default: False)
        
        Returns:
            Dict containing alignment results
        """
        try:
            import time
            from Bio import Align
            
            # Extract parameters
            sequence_a = params.get('sequence_a', '')
            sequence_b = params.get('sequence_b', '')
            score_only = params.get('score_only', False)
            one_alignment_only = params.get('one_alignment_only', False)
            
            # Validate inputs
            if not sequence_a or not sequence_b:
                return {"error": "Both sequences must be provided and non-empty"}
            
            if not isinstance(sequence_a, str) or not isinstance(sequence_b, str):
                return {"error": "Sequences must be strings"}
            
            # Perform local alignment with retry mechanism
            max_retries = 3
            retry_delay = 0.5  # seconds
            
            for attempt in range(max_retries):
                try:
                    # Create aligner with default parameters (match=1, mismatch=0, no gaps)
                    aligner = Align.PairwiseAligner()
                    aligner.mode = 'local'
                    aligner.match_score = 1.0
                    aligner.mismatch_score = 0.0
                    aligner.open_gap_score = 0.0
                    aligner.extend_gap_score = 0.0
                    
                    if score_only:
                        # Get only the score
                        score = aligner.score(sequence_a, sequence_b)
                        return {
                            "best_score": score,
                            "sequence_a": sequence_a,
                            "sequence_b": sequence_b,
                            "alignment_type": "local_simple"
                        }
                    
                    # Get alignments
                    alignments = aligner.align(sequence_a, sequence_b)
                    
                    # Convert to list and limit if requested
                    alignments_list = list(alignments)
                    if one_alignment_only and alignments_list:
                        alignments_list = alignments_list[:1]
                    
                    break  # Success, exit retry loop
                except Exception as retry_e:
                    if attempt < max_retries - 1 and ("Memory" in str(retry_e) or "timeout" in str(retry_e).lower()):
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    raise retry_e
            
            # Format results
            results = []
            for alignment in alignments_list:
                results.append({
                    "seq_a": str(alignment[0]),
                    "seq_b": str(alignment[1]),
                    "score": alignment.score,
                    "start": 0,  # Bio.Align doesn't provide start/end like pairwise2
                    "end": alignment.length,
                    "formatted": str(alignment)
                })
            
            return {
                "alignments": results,
                "best_score": results[0]["score"] if results else 0,
                "num_alignments": len(results),
                "sequence_a": sequence_a,
                "sequence_b": sequence_b,
                "alignment_type": "local_simple"
            }
            
        except Exception as e:
            error_msg = str(e)
            return {
                "error": f"Alignment failed: {error_msg}",
                "sequence_a": sequence_a,
                "sequence_b": sequence_b,
                "alignment_type": "local_simple"
            }
