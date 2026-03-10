"""
Test cases for Bio.SeqUtils Seq1 Tool.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_seq1 import BioSeqUtilsSeq1Tool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsSeq1Tool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsSeq1Tool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsSeq1Tool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "AlaGlyPhe"
        }

    def get_tool_instance(self):
        return BioSeqUtilsSeq1Tool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_conversion(self):
        """Test basic three-letter to one-letter conversion."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "AlaGlyPhe"
        })
        
        self.assertIn("converted_sequence", result)
        self.assertIn("conversion_type", result)
        self.assertEqual(result["conversion_type"], "three_letter_to_one_letter")

    def test_standard_amino_acids(self):
        """Test conversion of standard amino acids."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "MetLysLeuLeuValValSer"
        })
        
        self.assertNotIn("error", result)
        self.assertIn("converted_sequence", result)


if __name__ == '__main__':
    unittest.main()