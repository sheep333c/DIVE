"""
General web browsing tool for tools.

Provides web browsing and content extraction functionality.
"""

import json
from typing import Any, Dict

from tools.core.tool import Tool
from tools.core.types import ExecutionContext
from .utils.search_browse_utils import get_browse_results


class GeneralBrowseTool(Tool):
    """
    Tool for web browsing and content extraction.
    
    Description:
        Browses web pages and extracts content to answer specific questions.
        Uses AI-powered analysis to provide answers based on webpage content.
    
    Input Parameters:
        - url (str, required): URL of the webpage to browse
        - query (str, required): Question to answer based on the webpage content
    
    Output Format:
        Returns an AI-generated answer based on the webpage content.
        - Success: String answer to the query
        - Error: {"error": "error message"}
    """

    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        """Execute web browsing with given parameters."""
        try:
            # Extract required parameters 
            url = params.get("url", "")
            query = params.get("query", "")
            
            # Internal defaults - not exposed to model
            read_engine = "jina"
            max_retry = 3

            if not url.strip():
                return {"error": "URL parameter is required and cannot be empty"}

            if not query.strip():
                return {"error": "Query parameter is required and cannot be empty"}

            # Execute browsing
            result = get_browse_results(
                url=url,
                query=query,
                read_engine=read_engine,
                max_retry=max_retry,
            )
            
            return result
            
        except Exception as e:
            return {"error": f"Browse execution failed: {str(e)}"}
