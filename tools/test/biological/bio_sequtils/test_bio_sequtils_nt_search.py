"""
Test cases for Bio.SeqUtils NT Search Tool.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_nt_search import BioSeqUtilsNtSearchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsNtSearchTool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsNtSearchTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsNtSearchTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGATCGATCGATG",
            "subsequence": "GATC"
        }

    def get_tool_instance(self):
        return BioSeqUtilsNtSearchTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_nt_search(self):
        """Test basic nucleotide search."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGATCGATCGATG",
            "subsequence": "GATC"
        })
        
        self.assertIn("search_result", result)
        self.assertIn("sequence_length", result)
        self.assertIn("subsequence_length", result)
        self.assertIn("subsequence_searched", result)

    def test_restriction_site_search(self):
        """Test searching for restriction sites."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGAATTCGATCGAATTCATG",
            "subsequence": "GAATTC"  # EcoRI site
        })
        
        self.assertNotIn("error", result)
        self.assertEqual(result["subsequence_searched"], "GAATTC")


if __name__ == '__main__':
    unittest.main()