"""
Test cases for Bio.Seq Count Tool.

Tests the functionality of counting subsequences in biological sequences.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_count import BioSeqCountTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqCountTool(VerifiableToolTestBase):
    """Test cases for BioSeqCountTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqCountTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG",
            "overlap": False
        }

    def get_tool_instance(self):
        return BioSeqCountTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_count(self):
        """Test basic subsequence counting."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG"
        })
        
        self.assertIn("count", result)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["sequence_length"], 12)
        self.assertEqual(result["subsequence"], "ATG")

    def test_overlapping_count(self):
        """Test overlapping vs non-overlapping counts."""
        tool = self.get_tool_instance()
        
        # Non-overlapping (default)
        result1 = tool.execute(self.mock_ctx, {
            "sequence": "AAAA",
            "subsequence": "AAA",
            "overlap": False
        })
        self.assertEqual(result1["count"], 1)
        
        # Overlapping
        result2 = tool.execute(self.mock_ctx, {
            "sequence": "AAAA", 
            "subsequence": "AAA",
            "overlap": True
        })
        self.assertEqual(result2["count"], 2)

    def test_gc_content_analysis(self):
        """Test GC content related counting."""
        tool = self.get_tool_instance()
        
        # Count GC dinucleotides
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGCGCATGC",
            "subsequence": "GC"
        })
        
        self.assertIn("count", result)
        self.assertGreaterEqual(result["count"], 0)


if __name__ == '__main__':
    unittest.main()