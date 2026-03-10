#!/usr/bin/env python3
"""
NCBI Entrez ECitMatch工具测试
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.ncbi_entrez.ncbi_entrez_ecitmatch import NcbiEntrezEcitmatchTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestNcbiEntrezEcitmatchTool(VerifiableToolTestBase):
    """NCBI Entrez ECitMatch工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "NcbiEntrezEcitmatchTool"
    
    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        return {
            "bdata": "proc natl acad sci u s a|1991|88|3248|mann|Art1|"
        }
    
    def get_tool_instance(self):
        return NcbiEntrezEcitmatchTool()
    
    def get_execution_context(self):
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()