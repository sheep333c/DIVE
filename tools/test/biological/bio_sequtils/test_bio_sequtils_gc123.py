"""
Test cases for Bio.SeqUtils GC123 Tool.

Tests the functionality of calculating GC content by codon position.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_gc123 import BioSeqUtilsGc123Tool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsGc123Tool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsGc123Tool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsGc123Tool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGAAACGCTAG"
        }

    def get_tool_instance(self):
        return BioSeqUtilsGc123Tool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_gc123_calculation(self):
        """Test basic GC123 calculation."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGAAACGCTAG"  # 4 codons
        })
        
        self.assertIn("total_gc", result)
        self.assertIn("first_position_gc", result)
        self.assertIn("second_position_gc", result)
        self.assertIn("third_position_gc", result)
        self.assertIn("codon_count", result)
        self.assertEqual(result["codon_count"], 4)

    def test_high_gc_sequence(self):
        """Test sequence with high GC content."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "GCGCGCGCGCGC"  # All GC
        })
        
        self.assertEqual(result["total_gc"], 100.0)
        self.assertEqual(result["first_position_gc"], 100.0)
        self.assertEqual(result["second_position_gc"], 100.0)
        self.assertEqual(result["third_position_gc"], 100.0)

    def test_coding_sequence_example(self):
        """Test with a typical coding sequence."""
        tool = self.get_tool_instance()
        
        # Start codon + some codons + stop codon
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGTTCAAGTAA"  # ATG TTC AAG TAA
        })
        
        self.assertIn("total_gc", result)
        self.assertGreaterEqual(result["total_gc"], 0)
        self.assertLessEqual(result["total_gc"], 100)
        self.assertEqual(result["codon_count"], 4)


if __name__ == '__main__':
    unittest.main()