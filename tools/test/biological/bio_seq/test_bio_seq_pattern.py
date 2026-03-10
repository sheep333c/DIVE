"""
Test cases for Bio.Seq Pattern Tool.

Tests the functionality of pattern matching in biological sequences.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_pattern import BioSeqPatternTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqPatternTool(VerifiableToolTestBase):
    """Test cases for BioSeqPatternTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqPatternTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGATCGTAA",
            "pattern": "ATG",
            "operation": "startswith"
        }

    def get_tool_instance(self):
        return BioSeqPatternTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_startswith_pattern(self):
        """Test checking if sequence starts with pattern."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGTAA",
            "pattern": "ATG",
            "operation": "startswith"
        })
        
        self.assertIn("starts_with", result)
        self.assertTrue(result["starts_with"])
        self.assertTrue(result["matched"])
        self.assertEqual(result["pattern"], "ATG")

    def test_endswith_pattern(self):
        """Test checking if sequence ends with pattern."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGTAA",
            "pattern": "TAA",
            "operation": "endswith"
        })
        
        self.assertIn("ends_with", result)
        self.assertTrue(result["ends_with"])
        self.assertTrue(result["matched"])

    def test_both_patterns(self):
        """Test checking both start and end patterns."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "pattern": "ATG",
            "operation": "both"
        })
        
        self.assertIn("starts_with", result)
        self.assertIn("ends_with", result)
        self.assertTrue(result["starts_with"])
        self.assertTrue(result["ends_with"])
        self.assertTrue(result["matched_both"])

    def test_signal_peptide_check(self):
        """Test checking for signal peptide patterns."""
        tool = self.get_tool_instance()
        
        # Signal peptide often starts with hydrophobic amino acids
        result = tool.execute(self.mock_ctx, {
            "sequence": "MKLLVVSLLLLLLLLLLLEEQ",
            "pattern": "MK",
            "operation": "startswith"
        })
        
        self.assertTrue(result["starts_with"])

    def test_poly_a_tail(self):
        """Test checking for poly-A tail."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGAAAAAAA",
            "pattern": "AAAA",
            "operation": "endswith"
        })
        
        self.assertTrue(result["ends_with"])

    def test_pattern_not_found(self):
        """Test when pattern is not found."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGTAA",
            "pattern": "GGG",
            "operation": "startswith"
        })
        
        self.assertFalse(result["starts_with"])
        self.assertFalse(result["matched"])


if __name__ == '__main__':
    unittest.main()