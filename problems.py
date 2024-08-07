import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from tools import fetch_with_user_agent, scrape, search, find_relevant_articles, summarize

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

class SSSSS:
    def __init__(self, google_api_key, google_temperature, industry_name, type_client, region, problem_number, language, year, model):
        self.gpt_model = ChatGoogleGenerativeAI(api_key=google_api_key, model=model)
        self.google_api_key = google_api_key
        self.google_temperature = google_temperature
        self.industry_name = industry_name
        self.type_client = type_client
        self.region = region
        self.problem_number = problem_number
        self.language = language
        self.year = year
        self.model = model

    def call_google_chat(self, prompt):
        response = self.gpt_model.invoke(prompt)
        return response.content

    def generate_problem(self):
        # Extract URLs using tools.py
        query = f"current problems in the {self.industry_name} industry for {self.type_client} clients in {self.region}"
        search_results = search(query, self.year)
        urls = find_relevant_articles(search_results, query, self.gpt_model, self.problem_number)
        
        # Build the prompt with URLs
        url_list = "\n".join(urls)
        prompt = f"""
            You are an expert consultant in innovation specialized in applying the Lean Canvas. You have extensive experience in identifying critical problems within contemporary industries and markets. Your task is to identify {self.problem_number} current problems specifically faced by {self.type_client} clients in the {self.industry_name} industry in region {self.region}. You must conduct your research using the following sources:
            {url_list}
            Please respond only in the {self.language} language. Please present the results in a markdown table with four columns: 'Problème', 'Description', 'Impact', and 'Source'. Include the source URLs in the 'Source' column.
        """
        return self.call_google_chat(prompt)

    def execute(self):
        return self.generate_problem()

def localize_text(language):
    texts = {
        "English": {
            "title": "Problem Research",
            "subtitle": "Generate problems using AI",
            "input_details": "Enter the details below:",
            "industry": "Industry:",
            "client_type": "Client Type:",
            "region": "Region:",
            "num_problems": "Number of Problems:",
            "submit": "Submit",
            "result": "Here are the generated problems:",
            "year": "Enter the research year:"
        },
        "French": {
            "title": "Recherche de Problèmes",
            "subtitle": "Générez des problèmes à l'aide de l'IA",
            "input_details": "Entrez les détails ci-dessous :",
            "industry": "Industrie :",
            "client_type": "Type de client :",
            "region": "Région :",
            "num_problems": "Nombre de problèmes :",
            "submit": "Soumettre",
            "result": "Voici les problèmes générés :",
            "year": "Entrez l'année de recherche :"
        }
    }
    return texts[language]

def display_problems(api_key, temperature, lang, model):
    load_css('style.css')

    language = lang
    
    lang_texts = localize_text(language)
    
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["industry"]}</div>', unsafe_allow_html=True)
        industry_name = st.text_input('', 'Industrie plastique', key="industry_name_problems", label_visibility="collapsed")
    
    with col2:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["client_type"]}</div>', unsafe_allow_html=True)
        type_client = st.text_input('', 'Fabricants de moules ou moulistes', key="type_client_problems", label_visibility="collapsed")
    
    with col3:
        region_options = {
            'World': 'wt-wt',
            'Canada': 'ca-en',
            'United States': 'us-en',
            'United Kingdom': 'uk-en',
            'France': 'fr-fr',
            'Germany': 'de-de',
            'Spain': 'es-es',
            'Italy': 'it-it',
            'Japan': 'jp-ja',
            'Korea': 'kr-ko',
            'China': 'zh-cn'
        }
        region_display = list(region_options.keys())
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["region"]}</div>', unsafe_allow_html=True)
        region = st.selectbox("", region_display, key="region_problems")
        region_code = region_options[region]
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["year"]}</div>', unsafe_allow_html=True)
        year = st.number_input('', min_value=2000, max_value=2100, value=2024, key="year_problems", label_visibility="collapsed")
    
    with col5:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["num_problems"]}</div>', unsafe_allow_html=True)
        problem_number = st.number_input('', min_value=1, max_value=10, value=3, key="problem_number", label_visibility="collapsed")
    
    col7 = st.columns([1])
    with col7[0]:
        generate_button = st.button(lang_texts["submit"])

    if generate_button:
        if not api_key or not industry_name:
            st.warning(f"{lang_texts['api_key']} et {lang_texts['industry']}")
        else:
            try:             
                with st.spinner(lang_texts["result"]):
                    agent = SSSSS(api_key, temperature, industry_name, type_client, region_code, problem_number, language, year, model)
                    generated_problems = agent.generate_problem()

                    if isinstance(generated_problems, str):
                        st.markdown(generated_problems)
                        st.markdown("<br><br><br>", unsafe_allow_html=True)
                    else:
                        st.error("Problèmes générés ne sont pas sous forme de texte.")
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de la génération des problèmes pour l'industrie '{industry_name}' avec {problem_number} problèmes : {str(e)}")

