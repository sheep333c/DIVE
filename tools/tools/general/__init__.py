"""
General domain tools for tools.

This module provides general-purpose tools including:
- Web search functionality
- Web browsing and content extraction
- Parallel search capabilities
- Code execution
"""

from .search import GeneralSearchTool
from .browse import GeneralBrowseTool
from .parallel_search import GeneralParallelSearchTool
from .code_execution import CodeExecutionTool

# Backwards-compatible alias
GeneralCodeSandboxTool = CodeExecutionTool

__all__ = [
    'GeneralSearchTool',
    'GeneralBrowseTool',
    'GeneralParallelSearchTool',
    'CodeExecutionTool',
    'GeneralCodeSandboxTool',
]
