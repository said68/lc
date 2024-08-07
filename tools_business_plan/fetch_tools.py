import requests
from langchain.tools import tool

class FetchTools:
    @tool("fetch_with_user_agent")
    def fetch_with_user_agent(url: str) -> str:
        """Fetch a webpage with a user agent and return its content."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return "You do not have permission to access the requested page."
