"""
Test cases for Bio.SeqUtils Six Frame Tool.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_six_frame import BioSeqUtilsSixFrameTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsSixFrameTool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsSixFrameTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsSixFrameTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGAAACGCTAG"
        }

    def get_tool_instance(self):
        return BioSeqUtilsSixFrameTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_six_frame_translation(self):
        """Test basic six-frame translation."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGAAACGCTAG"
        })
        
        self.assertIn("translation_result", result)
        self.assertIn("sequence_length", result)
        self.assertIn("genetic_code_used", result)

    def test_with_genetic_code(self):
        """Test with different genetic code."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGAAACGCTAG",
            "genetic_code": 11
        })
        
        self.assertEqual(result["genetic_code_used"], 11)
        self.assertNotIn("error", result)


if __name__ == '__main__':
    unittest.main()