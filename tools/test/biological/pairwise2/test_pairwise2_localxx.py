"""
Test for Pairwise2LocalXX tool.
"""

from unittest.mock import MagicMock
from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.pairwise2.pairwise2_localxx import Pairwise2LocalXXTool
from tools.core.types import ExecutionContext


class TestPairwise2LocalXX(VerifiableToolTestBase):
    """Test class for Pairwise2LocalXX tool."""
    
    __test__ = True
    TOOL_CLASS_NAME = "Pairwise2LocalXXTool"
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        self.context = MagicMock(spec=ExecutionContext)
        self.context.request_id = "test_request_123"
        self.context.logger = MagicMock()
    
    def get_test_params(self):
        """Get test parameters for the tool."""
        return {
            "sequence_a": "ATGCGATCG",
            "sequence_b": "ATGCGATCG",
            "score_only": False,
            "one_alignment_only": True,
            "penalize_end_gaps": False,
            "gap_char": "-"
        }
    
    def get_tool_instance(self):
        """Get tool instance for testing."""
        return Pairwise2LocalXXTool()
    
    def get_execution_context(self):
        """Get execution context for testing."""
        return self.context