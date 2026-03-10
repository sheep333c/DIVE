"""
General web search tool for tools.

Provides web search functionality using various search engines.
"""

import json
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from .utils.search_browse_utils import get_search_results


class GeneralSearchTool(Tool):
    """
    Tool for general web search functionality.
    
    Description:
        Performs web searches and returns formatted results with titles, URLs, and snippets.
        Supports advanced search syntax like site:, inurl:, intitle:, etc.
    
    Input Parameters:
        - query (str, required): Search query string
    
    Output Format:
        Returns search results as formatted text with titles, URLs, and snippets.
        - Success: Formatted string with search results
        - Error: {"error": "error message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """Execute web search with given parameters."""
        try:
            # Extract required parameter
            query = params.get("query", "")
            
            # Internal defaults - not exposed to model
            topk = 3
            max_retry = 1
            engine = "serper"
            max_length = 10000
            
            if not query.strip():
                return {"error": "Query parameter is required and cannot be empty"}
            
            # Execute search
            result = get_search_results(
                query=query,
                topk=topk,
                max_retry=max_retry,
                engine=engine
            )
            
            # Clip result to max length if specified
            if max_length and len(result) > max_length:
                result = result[:max_length] + "... [truncated]"
            
            return result
            
        except Exception as e:
            return {"error": f"Search execution failed: {str(e)}"}
