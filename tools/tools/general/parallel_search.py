"""
General parallel search tool for tools.

Provides parallel web search functionality for multiple queries.
"""

import json
from typing import Any, Dict, List

from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from .utils.search_browse_utils import get_search_results_parallel


class GeneralParallelSearchTool(Tool):
    """
    Tool for parallel web search functionality.
    
    Description:
        Performs multiple web searches in parallel and returns combined results.
        Useful for gathering information from multiple related queries simultaneously.
    
    Input Parameters:
        - queries (list, required): Array of search query strings to execute in parallel
    
    Output Format:
        Returns combined search results with clear separation between queries.
        - Success: Formatted string with all search results
        - Error: {"error": "error message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """Execute parallel web searches with given parameters."""
        try:
            # Extract required parameter
            queries = params.get("queries", [])
            
            # Internal defaults - not exposed to model
            topk = 3
            max_retry = 1
            engine = "serper"
            
            if not queries or not isinstance(queries, list):
                return {"error": "Queries parameter is required and must be a non-empty list"}
            
            if not all(isinstance(q, str) and q.strip() for q in queries):
                return {"error": "All queries must be non-empty strings"}
            
            # Execute parallel searches
            result = get_search_results_parallel(
                queries=queries,
                topk=topk,
                max_retry=max_retry,
                engine=engine
            )
            
            return result
            
        except Exception as e:
            return {"error": f"Parallel search execution failed: {str(e)}"}
