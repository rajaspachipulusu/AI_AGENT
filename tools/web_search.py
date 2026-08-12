import json

from ddgs import DDGS


class WebSearchTool:

    name = "web_search"

    description = """
    Searches the internet for current or external information.

    Use this tool when the user asks about:

    - Latest information
    - Current events
    - Recent technology versions
    - News
    - Information not available in the CSV
    - General web information

    Input format:

    {
        "query": "search query"
    }

    Example:

    {
        "query": "latest Python version"
    }
    """

    @staticmethod
    def run(tool_input):

        try:

            # ----------------------------------
            # Parse tool input
            # ----------------------------------

            if isinstance(tool_input, str):

                tool_input = json.loads(
                    tool_input
                )

            # ----------------------------------
            # Get search query
            # ----------------------------------

            query = tool_input.get("query")

            if not query:

                return {
                    "status": "error",
                    "message": (
                        "Search query is required."
                    )
                }

            # ----------------------------------
            # Perform Web Search
            # ----------------------------------

            results = []

            with DDGS() as ddgs:

                search_results = ddgs.text(
                    query,
                    max_results=5
                )

                for result in search_results:

                    results.append({
                        "title": result.get("title"),
                        "url": result.get("href"),
                        "snippet": result.get("body")
                    })

            # ----------------------------------
            # Return Results
            # ----------------------------------

            return {
                "status": "success",
                "query": query,
                "results": results
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }