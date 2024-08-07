import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import fetch_with_user_agent, scrape, search, find_relevant_articles, summarize
from typing import List, Dict

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

class Solutions:
    def __init__(self, google_api_key, google_temperature, industry_name, problem_description, num_solutions, language, year, model, creative_method):
        self.gpt_model = ChatGoogleGenerativeAI(api_key=google_api_key, model=model)
        self.google_api_key = google_api_key
        self.google_temperature = google_temperature
        self.industry_name = industry_name
        self.problem_description = problem_description
        self.num_solutions = num_solutions
        self.language = language
        self.year = year
        self.model = model
        self.creative_method = creative_method

    def call_google_chat(self, prompt):
        response = self.gpt_model.invoke(prompt)
        if response and response.content:
            return response.content
        else:
            raise ValueError("Invalid response from Google API")

    def generate_existing_solutions(self):
        query = f"current solutions for the {self.problem_description} in the {self.industry_name} industry"
        search_results = search(query, self.year)
        urls = find_relevant_articles(search_results, query, self.gpt_model, self.num_solutions)

        # Build the prompt with URLs
        url_list = "\n".join(urls)
        prompt = f"""
            You are an expert consultant in innovation specializing in applying the Lean Canvas. Your task is to identify {self.num_solutions} existing solutions to solve the following problem in the {self.industry_name} industry: {self.problem_description}. Please conduct your research using the following sources:
            {url_list}
            Please respond only in the {self.language} language. Please present the results in a markdown table with three columns: 'Solution', 'Description', and 'Source'. Include the source URLs in the 'Source' column.
        """
        return self.call_google_chat(prompt)

    def generate_creative_solutions(self):
        if self.creative_method == "Five Whys":
            prompt = f"""
                Step into the role of an expert consultant in innovation. Pinpoint the initial problem within the {self.problem_description} in the {self.industry_name} industry, and continuously question 'why?' the problem exists, getting five layers deep to expose the fundamental reason. Document your findings and propose {self.num_solutions} actionable solutions. Please respond only in the {self.language} language. Present the results in a markdown table with four columns: 'Solution', 'Description', 'Unique Value Proposition', and 'Customer Segment'.
            """
        elif self.creative_method == "Scamper":
            prompt = f"""
                Using the SCAMPER framework, generate {self.num_solutions} innovative ideas to improve the {self.problem_description} in the {self.industry_name} industry. Consider each SCAMPER element: Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, and Reverse. Document your findings and proposed solutions. Please respond only in the {self.language} language. Present the results in a markdown table with four columns: 'Solution', 'Description', 'Unique Value Proposition', and 'Customer Segment'.
            """
        elif self.creative_method == "Triz":
            prompt = f"""
                Embrace the mindset of an expert consultant in innovation. Apply the TRIZ framework to creatively address {self.problem_description} in the {self.industry_name} industry. Seek out and reconcile paradoxes, leveraging TRIZ's standards to formulate {self.num_solutions} breakthrough solutions. Detail your process and the application of TRIZ concepts in your strategy. Please respond only in the {self.language} language. Present the results in a markdown table with four columns: 'Solution', 'Description', 'Unique Value Proposition', and 'Customer Segment'.
            """
        return self.call_google_chat(prompt)

    def execute(self):
        try:
            existing_solutions = self.generate_existing_solutions()
            creative_solutions = self.generate_creative_solutions()
        except ValueError as e:
            st.error(f"Error generating solutions: {str(e)}")
            return None, None

        return existing_solutions, creative_solutions

def localize_text(language):
    texts = {
        "English": {
            "title": "Solutions",
            "subtitle": "Generate solutions using AI",
            "input_details": "Enter the details below:",
            "industry_name": "Industry:",
            "problem_description": "Problem Description:",
            "num_solutions": "Number of Solutions:",
            "creative_method": "Creative Method:",
            "submit": "Submit",
            "result": "Here are the generated solutions:",
            "year": "Enter the research year:"
        },
        "French": {
            "title": "Solutions",
            "subtitle": "Générez des solutions à l'aide de l'IA",
            "input_details": "Entrez les détails ci-dessous :",
            "industry_name": "Industrie :",
            "problem_description": "Description du Problème :",
            "num_solutions": "Nombre de Solutions :",
            "creative_method": "Méthode créative :",
            "submit": "Soumettre",
            "result": "Voici les solutions générés :",
            "year": "Entrez l'année de recherche :"
        }
    }
    return texts[language]

def display_solutions(api_key, temperature, lang, model):
    load_css('style.css')

    language = lang
    
    lang_texts = localize_text(language)
    
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["industry_name"]}</div>', unsafe_allow_html=True)
        industry_name = st.text_input('', 'Industrie plastique', key="industry_name_solutions", label_visibility="collapsed")
    
    with col2:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["problem_description"]}</div>', unsafe_allow_html=True)
        problem_description = st.text_input('', 'Rareté des employés', key="problem_description_solutions", label_visibility="collapsed")
    
    with col3:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["num_solutions"]}</div>', unsafe_allow_html=True)
        num_solutions = st.number_input('', min_value=1, max_value=10, value=3, key="num_solutions_solutions", label_visibility="collapsed")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["year"]}</div>', unsafe_allow_html=True)
        year = st.number_input('', min_value=2000, max_value=2100, value=2024, key="year_solutions", label_visibility="collapsed")

    with col5:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["creative_method"]}</div>', unsafe_allow_html=True)
        creative_method = st.selectbox("", ["Five Whys", "Scamper", "Triz"], key="creative_method_solutions", label_visibility="collapsed")
    
    col7 = st.columns([1])
    with col7[0]:
        generate_button = st.button(lang_texts["submit"], key="submit_solutions")

    if generate_button:
        if not api_key or not industry_name or not problem_description:
            st.warning(f"{lang_texts['industry_name']}, et {lang_texts['problem_description']}")
        else:
            try:
                with st.spinner(lang_texts["result"]):
                    agent = Solutions(api_key, temperature, industry_name, problem_description, num_solutions, language, year, model, creative_method)
                    existing_solutions, creative_solutions = agent.execute()

                    if existing_solutions is None or creative_solutions is None:
                        st.error("Problèmes générés ne sont pas sous forme de texte.")
                    else:
                        # Display existing solutions
                        st.markdown("### Existing Solutions")
                        st.markdown(existing_solutions)

                        # Display creative solutions
                        st.markdown("### Creative Solutions")
                        st.markdown(creative_solutions)
                    
                    st.markdown("<br><br><br>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Une erreur est survenue lors de la génération des solutions pour l'industrie '{industry_name}' avec {num_solutions} solutions : {str(e)}")

