#!/usr/bin/env python3
"""
NCBI Entrez ESpell工具测试
"""

import unittest
from unittest.mock import MagicMock
from tools.biological.ncbi_entrez.ncbi_entrez_espell import NcbiEntrezEspellTool
from tools.core.types import ExecutionContext
from test.base_verifiable_tool_test import VerifiableToolTestBase


class TestNcbiEntrezEspellTool(VerifiableToolTestBase):
    """NCBI Entrez ESpell工具测试"""
    
    __test__ = True
    TOOL_CLASS_NAME = "NcbiEntrezEspellTool"
    
    def setUp(self):
        super().setUp()
        self.mock_ctx = MagicMock(spec=ExecutionContext)
        self.mock_ctx.timeout_ms = 30000
    
    def get_test_params(self):
        return {
            "term": "biopythn",  # 故意拼错的单词
            "db": "pubmed"
        }
    
    def get_tool_instance(self):
        return NcbiEntrezEspellTool()
    
    def get_execution_context(self):
        return self.mock_ctx


if __name__ == '__main__':
    unittest.main()