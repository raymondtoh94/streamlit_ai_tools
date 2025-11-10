"""
Web Search Tool using TavilySearch
"""

from langchain.tools import tool
from langchain_tavily import TavilySearch


@tool
def web_search(query: str, limit: int = 5) -> str:
    """
    Perform a web search using TavilySearch.
    Args:
        query (str): The search query.
        limit (int): The maximum number of results to return.
    Returns:
        str: The search results.
    """

    search = TavilySearch(max_results=limit)
    return search.invoke(f"""{query}""")
