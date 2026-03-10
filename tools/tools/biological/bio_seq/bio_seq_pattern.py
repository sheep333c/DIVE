"""
Bio.Seq Pattern Tool - Check sequence pattern matching using startswith/endswith.

This tool provides sequence pattern matching functionality using BioPython's Bio.Seq module.
Useful for checking signal peptides, poly-A tails, promoter regions, and other sequence features.
"""

from typing import Dict, Any
from Bio.Seq import Seq
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class BioSeqPatternTool(Tool):
    """Tool for pattern matching in biological sequences."""

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if sequence starts with or ends with specific patterns.
        
        Args:
            params: Dictionary containing:
                - sequence (str): Input nucleotide or protein sequence
                - pattern (str): Pattern to match
                - operation (str): 'startswith', 'endswith', or 'both'
                - start (int, optional): Start position for startswith check
                - end (int, optional): End position for endswith check
                
        Returns:
            Dictionary with pattern matching results or error message
        """
        try:
            sequence = params.get('sequence')
            pattern = params.get('pattern')
            operation = params.get('operation', 'startswith')
            start = params.get('start', 0)
            end = params.get('end')
            
            if not sequence:
                return {"error": "Missing required parameter: sequence"}
            if not pattern:
                return {"error": "Missing required parameter: pattern"}
                
            # Clean sequences
            clean_sequence = ''.join(sequence.upper().split())
            clean_pattern = ''.join(pattern.upper().split())
            
            if not clean_pattern:
                return {"error": "Pattern cannot be empty"}
                
            # Validate operation
            valid_operations = ['startswith', 'endswith', 'both']
            if operation not in valid_operations:
                return {"error": f"Invalid operation: {operation}. Must be one of {valid_operations}"}
                
            # Create Seq object
            seq_obj = Seq(clean_sequence)
            seq_length = len(clean_sequence)
            
            # Validate positions
            if start < 0:
                start = 0
            if end is None:
                end = seq_length
            elif end > seq_length:
                end = seq_length
                
            result = {
                "sequence_length": seq_length,
                "pattern": clean_pattern,
                "pattern_length": len(clean_pattern),
                "operation": operation
            }
            
            if operation == 'startswith':
                # Check if sequence starts with pattern (from given start position)
                starts_with = seq_obj.startswith(clean_pattern, start)
                result.update({
                    "starts_with": starts_with,
                    "start_position": start,
                    "matched": starts_with
                })
                
            elif operation == 'endswith':
                # Check if sequence ends with pattern (up to given end position)  
                ends_with = seq_obj.endswith(clean_pattern, 0, end)
                result.update({
                    "ends_with": ends_with,
                    "end_position": end,
                    "matched": ends_with
                })
                
            elif operation == 'both':
                # Check both start and end patterns
                starts_with = seq_obj.startswith(clean_pattern, start)
                ends_with = seq_obj.endswith(clean_pattern, 0, end)
                result.update({
                    "starts_with": starts_with,
                    "ends_with": ends_with,
                    "start_position": start,
                    "end_position": end,
                    "matched_start": starts_with,
                    "matched_end": ends_with,
                    "matched_both": starts_with and ends_with
                })
            
            return result
            
        except Exception as e:
            return {"error": f"Pattern matching failed: {str(e)}"}
