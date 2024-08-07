import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import json
from typing import Optional, List, Dict

def fetch_with_user_agent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def scrape(url):
    html_content = fetch_with_user_agent(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text()
        return text_content
    else:
        return "You do not have permission to access the requested page."

def summarize(document_text, gpt_model, temperature, language, url, query):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"],
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
    )
    texts = text_splitter.split_text(document_text)
    
    if language == 'French':
        summary_template = f"""
        Écrire un post détaillé sur le sujet "{query}" en incluant le lien trouvé comme référence dans l'article.
        {{texts}}
        LIEN:
        {url}
        POST DÉTAILLÉ :
        """
    else:
        summary_template = f"""
        Write a detailed post on the topic "{query}" including the link found as a reference within the article.
        {{texts}}
        LINK:
        {url}
        DETAILED POST:
        """
    
    prompt = PromptTemplate(
        input_variables=['texts'],
        template=summary_template
    )
    chain = LLMChain(prompt=prompt, llm=gpt_model)

    documents = [Document(page_content=text) for text in texts]
    stuff_chain = load_summarize_chain(llm=gpt_model, chain_type="stuff")
    return stuff_chain.run(input_documents=documents)

def search(query: str, year: int, region: Optional[str] = "wt-wt", safesearch: str = "moderate") -> List[Dict]:
    ddgs = DDGS()
    results = ddgs.text(f"{query} {year}", region=region, safesearch=safesearch)
    return results

def find_relevant_articles(response, query, gpt_model, num_articles=6):
    response_data = json.dumps(response)
    template = f"""
    You are the best researcher of all time. You are extremely good at finding the relevant articles to the query.
    {{response_data}}
    Above is the list of search results of articles for the query: {{query}}.
    Please rank the best {num_articles} articles from the list, return ONLY an array of the urls, do not include any information.
    Return ONLY an array of the urls, do not include anything else.
    """

    prompt = PromptTemplate(
        input_variables=['response_data', 'query'],
        template=template
    )

    chain = LLMChain(prompt=prompt, llm=gpt_model)
    urls = chain.run(response_data=response_data, query=query)
    url_list = json.loads(urls)
    return url_list
