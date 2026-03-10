"""
Test cases for Bio.Seq Find Tool.

Tests the functionality of finding subsequence positions in biological sequences.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_seq.bio_seq_find import BioSeqFindTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqFindTool(VerifiableToolTestBase):
    """Test cases for BioSeqFindTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqFindTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG",
            "find_all": False
        }

    def get_tool_instance(self):
        return BioSeqFindTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_find_first_occurrence(self):
        """Test finding first occurrence of subsequence."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG"
        })
        
        self.assertIn("position", result)
        self.assertEqual(result["position"], 0)
        self.assertTrue(result["found"])
        self.assertEqual(result["sequence_length"], 12)

    def test_find_all_occurrences(self):
        """Test finding all occurrences of subsequence."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG",
            "find_all": True
        })
        
        self.assertIn("positions", result)
        self.assertIn("count", result)
        self.assertEqual(result["positions"], [0, 9])
        self.assertEqual(result["count"], 2)
        self.assertTrue(result["found"])

    def test_restriction_site_search(self):
        """Test finding restriction enzyme sites."""
        tool = self.get_tool_instance()
        
        # EcoRI site (GAATTC) search
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGAATTCGATCGAATTCATG",
            "subsequence": "GAATTC",
            "find_all": True
        })
        
        self.assertIn("positions", result)
        self.assertEqual(len(result["positions"]), 2)
        self.assertTrue(result["found"])

    def test_range_search(self):
        """Test searching within specific sequence range."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "subsequence": "ATG",
            "start": 5,
            "end": 12
        })
        
        self.assertIn("position", result)
        self.assertEqual(result["position"], 9)
        self.assertEqual(result["search_range"], [5, 12])

    def test_not_found(self):
        """Test when subsequence is not found."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATG",
            "subsequence": "TTT"
        })
        
        self.assertEqual(result["position"], -1)
        self.assertFalse(result["found"])


if __name__ == '__main__':
    unittest.main()