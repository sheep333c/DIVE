"""
Test cases for Bio.SeqUtils GC Content Tool.

Tests the functionality of calculating GC content in biological sequences.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_gc_content import BioSeqUtilsGcContentTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsGcContentTool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsGcContentTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsGcContentTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGCGCATGC",
            "ambiguous": "ignore"
        }

    def get_tool_instance(self):
        return BioSeqUtilsGcContentTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_gc_content(self):
        """Test basic GC content calculation."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGCGCATGC"
        })
        
        self.assertIn("gc_content", result)
        self.assertIn("gc_fraction", result)
        self.assertIn("sequence_length", result)
        
        # Should be high GC content (8 GC out of 12 = 66.67%)
        self.assertGreater(result["gc_content"], 60)

    def test_low_gc_content(self):
        """Test sequence with low GC content."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "AAATTTAAATTT"  # All A and T
        })
        
        self.assertEqual(result["gc_content"], 0.0)

    def test_ambiguous_handling(self):
        """Test different ambiguous nucleotide handling."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCRYWS",
            "ambiguous": "ignore"
        })
        
        self.assertIn("gc_content", result)
        self.assertNotIn("error", result)


if __name__ == '__main__':
    unittest.main()