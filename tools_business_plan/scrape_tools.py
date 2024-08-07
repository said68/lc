from bs4 import BeautifulSoup
from langchain.tools import tool
from tools_business_plan.fetch_tools import FetchTools

class ScrapeTools:
    @tool("scrape")
    def scrape(url: str) -> str:
        """Scrape a webpage and return its text content."""
        html_content = FetchTools.fetch_with_user_agent(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()
            return text_content
        else:
            return "You do not have permission to access the requested page."
