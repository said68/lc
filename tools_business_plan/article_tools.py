import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import tool

class ArticleTools:
    @tool("find_relevant_articles")
    def find_relevant_articles(response, query, gpt_model, num_articles=6) -> str:
        """Find relevant articles from search results."""
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

