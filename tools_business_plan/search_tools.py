import json
from langchain.tools import tool
from duckduckgo_search import DDGS

class SearchTools:
    @tool("search")
    def search_internet(query: str, year: int, region: str = "wt-wt", safesearch: str = "moderate") -> str:
        """Search the internet for a given topic and return relevant results."""
        ddgs = DDGS()
        results = ddgs.text(f"{query} {year}", region=region, safesearch=safesearch)

        if not results:
            return "Sorry, I couldn't find anything about that, there could be an error with your search tool."

        result_strings = []
        for result in results:
            try:
                result_strings.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['href']}",
                    f"Snippet: {result['body']}",
                    "\n-----------------"
                ]))
            except KeyError:
                continue

        return '\n'.join(result_strings)
