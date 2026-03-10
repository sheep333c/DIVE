"""
Test cases for Bio.SeqUtils GC Skew Tool.
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.bio_sequtils.bio_sequtils_gc_skew import BioSeqUtilsGcSkewTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestBioSeqUtilsGcSkewTool(VerifiableToolTestBase):
    """Test cases for BioSeqUtilsGcSkewTool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "BioSeqUtilsGcSkewTool"

    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000

    def get_test_params(self):
        return {
            "sequence": "ATGCGCGCATGCGCGCATGCGCGCATGC",
            "window": 10
        }

    def get_tool_instance(self):
        return BioSeqUtilsGcSkewTool()

    def get_execution_context(self):
        return self.mock_ctx

    def test_basic_gc_skew(self):
        """Test basic GC skew calculation."""
        tool = self.get_tool_instance()
        
        result = tool.execute(self.mock_ctx, {
            "sequence": "ATGCGCGCATGCGCGCATGCGCGCATGC",
            "window": 10
        })
        
        self.assertIn("gc_skew_values", result)
        self.assertIn("window_size", result)
        self.assertIn("window_count", result)
        self.assertEqual(result["window_size"], 10)

    def test_different_window_sizes(self):
        """Test with different window sizes."""
        tool = self.get_tool_instance()
        sequence = "ATGCGCGCATGCGCGCATGCGCGCATGC" * 2
        
        for window in [5, 10, 20]:
            result = tool.execute(self.mock_ctx, {
                "sequence": sequence,
                "window": window
            })
            
            self.assertEqual(result["window_size"], window)
            self.assertIsInstance(result["gc_skew_values"], list)


if __name__ == '__main__':
    unittest.main()