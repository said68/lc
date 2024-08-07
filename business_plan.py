import os
import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from tools_business_plan.search_tools import SearchTools
from tools_business_plan.fetch_tools import FetchTools
from tools_business_plan.scrape_tools import ScrapeTools
from tools_business_plan.summarize_tools import SummarizeTools
from tools_business_plan.article_tools import ArticleTools
from tools_business_plan.calculate_tools import CalculateTools
from crewai import Agent, Task, Process, Crew

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def localize_text(language):
    texts = {
        "English": {
            "title": "Business Plan",
            "company_name": "Company Name",
            "target_customer": "Target Customer",
            "industry": "Industry",
            "description": "Company Description",
            "year": "Year",
            "region": "Region",
            "cogs_percentage": "COGS Percentage",
            "expenses_percentage": "Expenses Percentage",
            "submit": "Submit",
            "processing": "Generating business plan...",
            "result_title": "Here is your Business Plan:"
        },
        "French": {
            "title": "Plan d'affaires",
            "company_name": "Nom de l'entreprise",
            "target_customer": "Client Cible",
            "industry": "Industrie",
            "description": "Description de l'entreprise",
            "year": "Année",
            "region": "Région",
            "cogs_percentage": "Pourcentage des COGS",
            "expenses_percentage": "Pourcentage des dépenses",
            "submit": "Soumettre",
            "processing": "Génération du plan d'affaires en cours...",
            "result_title": "Voici votre Plan d'Affaires :"
        }
    }
    return texts[language]

def display_business_plan(api_key, temperature, lang, model):
    load_css('style.css')
    
    lang_texts = localize_text(lang)
    
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["company_name"]}</div>', unsafe_allow_html=True)
        company_name = st.text_input('', 'Plas', key="company_name", label_visibility="collapsed")
    
    with col2:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["target_customer"]}</div>', unsafe_allow_html=True)
        target_customer = st.text_input('', 'Fabricants de plastique', key="target_customer", label_visibility="collapsed")
    
    with col3:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["industry"]}</div>', unsafe_allow_html=True)
        industry = st.text_input('', 'Plastique', key="industry", label_visibility="collapsed")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["description"]}</div>', unsafe_allow_html=True)
        description = st.text_input('', 'Entreprise qui fabrique les moules en acier pour les entreprises de plastique', key="description", label_visibility="collapsed")
    
    with col5:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["year"]}</div>', unsafe_allow_html=True)
        year = st.number_input('', min_value=2000, max_value=2100, value=2024, key="year", label_visibility="collapsed")
    
    with col6:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["region"]}</div>', unsafe_allow_html=True)
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
        region = st.selectbox('', list(region_options.keys()), index=0, key="region", label_visibility="collapsed")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["cogs_percentage"]}</div>', unsafe_allow_html=True)
        cogs_percentage = st.number_input('', min_value=0.0, max_value=100.0, value=20.0, step=0.1, key="cogs_percentage", label_visibility="collapsed")
    
    with col8:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["expenses_percentage"]}</div>', unsafe_allow_html=True)
        expenses_percentage = st.number_input('', min_value=0.0, max_value=100.0, value=15.0, step=0.1, key="expenses_percentage", label_visibility="collapsed")
    
    submit_button = st.button(lang_texts["submit"], key="submit_button_business_plan")
    
    if submit_button:
        with st.spinner(lang_texts["processing"]):
            llm = ChatGoogleGenerativeAI(api_key=api_key, model=model, temperature=temperature)

            market_agent = Agent(
                role="Market Research Analyst",
                goal=f"""Conduct a detailed market analysis for the {industry} industry and targeting {target_customer} to ensure the business {description} is backed by solid research and data.""",
                backstory=f"""You are an expert in understanding market demand, demand estimation, target audience, and competition in the {industry} industry. You are skilled at doing market research for a given {description}". YOu have worked with numerous startups and established companies, helping them identify market trends and develop successful business strategies.primary mission is to help the company {company_name}. Please respond only in {lang}. You must Include references to external data for market analysis""",
                allow_delegation=False,
                tools=[SearchTools().search_internet, FetchTools().fetch_with_user_agent, ScrapeTools().scrape, SummarizeTools().summarize],
                llm=llm,
                verbose=True
            )
    
            technology_agent = Agent(
                role="Technology Expert",
                goal=f"""Assess the technological feasibility and necessary technologies for the {industry} industry.""",
                backstory=f"""You are a visionary in technology with a deep understanding of technological trends especially in products like {description}. Your expertise is crucial for aligning technology with business strategies. Please respond only in {lang}.""",
                allow_delegation=False,
                tools=[SearchTools().search_internet, FetchTools().fetch_with_user_agent, ScrapeTools().scrape, SummarizeTools().summarize],
                llm=llm,
                verbose=True
            )
    
            financial_agent = Agent(
                role="Profitability Analyst",
                goal=f"""Establish the cashflow prediction for the company.""",
                backstory=f"""You are an expert in financial analysis. Your mission is to build financial projections for {company_name}, indicating robust growth over the next three years. Please respond only in {lang}.""",
                allow_delegation=False,
                tools=[SearchTools().search_internet, FetchTools().fetch_with_user_agent, ScrapeTools().scrape, SummarizeTools().summarize],
                llm=llm,
                verbose=True
            )
    
            business_consultant = Agent(
                role="Business Development Consultant",
                goal= f"""Evaluate the business model for {description}, focusing on scalability and revenue streams.""",
                backstory=f"""Expert in shaping business strategies for products like {description} in {industry} industry. 
                      Understands scalability and potential revenue streams to ensure long-term sustainability""",
                allow_delegation=True,
                tools=[SearchTools().search_internet, FetchTools().fetch_with_user_agent, ScrapeTools().scrape, SummarizeTools().summarize],
                llm=llm,
                verbose=True
            )
    
            task1 = Task(
                description=f"""Conduct a detailed market analysis for the {industry} industry, targeting {target_customer} for {description}.
                 Current year is {year} and the target customer is in {region}. Write a report on the ideal customer profile, demande estimation in canadian dollars and marketing 
                 strategies to reach the widest possible audience. Include at least 10 bullet points addressing key marketing areas. Please respond only in {lang}.
                          
                """,
                agent=market_agent,
                expected_output="Market analysis including demand size in canadian dollars, demand trends, ideal customer profile and segements."
            )
    
            task2 = Task(
                description=f"""Assess the technological feasibility and necessary technologies for the {industry} industry for {description} .
                 Write a report detailing necessary technologies and manufacturing approaches. Include at least 10 bullet points on key technological areas.
                 Please respond only in {lang}.
                """,
                agent=technology_agent,
                expected_output="Technological assessment including required technologies and their implementation."
            )
    
            task3 = Task(
                description=f"""Establish financial projections and build an income statement.
                Write a report detailing necessary financial and profitability of the {company_name} if it launch the {description}. 
                Include at least 10 bullet points on key financial and profitability issues to consider by the {company_name}.
                 Please respond only in {lang}.
                """,
                agent=financial_agent,
                expected_output="Detailed financial projections including revenue, COGS, gross profit, expenses, net income, and detailled issues and recommendations to consider."
            )
    
            task4 = Task(
                description=f""" Analyze and summarize marketing, technological, and financial reports and write a detailed business plan 
                describing how to make sustainable and profitable for {description}. The business plan has to be concise with at least ten bullet points and five goals and must contain 
                a schedule for which goals should be achieved and when starting no earlier than next {year}. Please respond only in {lang}.
                """,
                agent=business_consultant,
                context = [task1, task2,task3], 
                expected_output="A detailed business plan that integrates the marketing, technological, and financial reports, outlining a sustainable and profitable business model for the product."
            )
    
            crew = Crew(
                agents=[market_agent, technology_agent, financial_agent, business_consultant],
                tasks=[task1, task2, task3, task4],
                verbose=2,
                process=Process.sequential
            )
    
            result = crew.kickoff()
    
            st.subheader(lang_texts["result_title"])
            st.markdown(result)

if __name__ == "__main__":
    display_business_plan(api_key="your_api_key_here", temperature=0.5, lang="French", model="gemini-1.5-pro-latest")
