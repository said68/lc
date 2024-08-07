from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.tools import tool

class SummarizeTools:
    @tool("summarize")
    def summarize(document_text: str, gpt_model, temperature: float, language: str, url: str, query: str) -> str:
        """Summarize a given document text."""
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

