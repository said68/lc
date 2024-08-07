import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

class LeanCanvas:
    def __init__(self, google_api_key, google_temperature, industry_name, problem_description, solution_description, language, year, model):
        self.gpt_model = ChatGoogleGenerativeAI(api_key=google_api_key, model=model)
        self.google_api_key = google_api_key
        self.google_temperature = google_temperature
        self.industry_name = industry_name
        self.problem_description = problem_description
        self.solution_description = solution_description
        self.language = language
        self.year = year
        self.model = model

    def call_google_chat(self, prompt):
        response = self.gpt_model.invoke(prompt)
        return response.content

    def generate_lean_canvas(self):
        prompt = f"""
            You are an expert consultant in innovation specializing in applying the Lean Canvas. Your task is to create a detailed Lean Canvas for the following problem and solution in the {self.industry_name} industry: Problem: {self.problem_description}. Solution: {self.solution_description}. Please respond only in the {self.language} language. Present the Lean Canvas in a markdown table with the following sections: 'Customer Segments', 'Value Propositions', 'Channels', 'Revenue Streams', 'Cost Structure', 'Key Metrics', and 'Competitive Advantages'.
        """
        return self.call_google_chat(prompt)

    def execute(self):
        lean_canvas = self.generate_lean_canvas()
        return lean_canvas

def localize_text(language):
    texts = {
        "English": {
            "title": "Lean Canvas",
            "subtitle": "Generate your Lean Canvas using AI",
            "input_details": "Enter the details below:",
            "industry": "Industry:",
            "problem_description": "Problem Description:",
            "solution_description": "Solution Description:",
            "confirm_problem_solution": "Confirm or Modify Problem and Solution",
            "problem": "Problem",
            "solution": "Solution",
            "confirm": "Confirm",
            "submit": "Submit",
            "result": "Here is your Lean Canvas:"
        },
        "French": {
            "title": "Lean Canvas",
            "subtitle": "Générez votre Lean Canvas à l'aide de l'IA",
            "input_details": "Entrez les détails ci-dessous :",
            "industry": "Industrie :",
            "problem_description": "Description du Problème :",
            "solution_description": "Description de la Solution :",
            "confirm_problem_solution": "Confirmez ou Modifiez le Problème et la Solution",
            "problem": "Problème",
            "solution": "Solution",
            "confirm": "Confirmer",
            "submit": "Soumettre",
            "result": "Voici votre Lean Canvas :"
        }
    }
    return texts[language]

def display_lean_canvas(api_key, temperature, lang, model):
    load_css('style.css')

    language = lang
    lang_texts = localize_text(language)
    
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if "confirmed" not in st.session_state:
        st.session_state.confirmed = False

    if not st.session_state.confirmed:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["industry"]}</div>', unsafe_allow_html=True)
            industry_name = st.text_input('', 'Industrie plastique', key="industry_name_lean_canvas", label_visibility="collapsed")
        
        with col2:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["problem_description"]}</div>', unsafe_allow_html=True)
            problem_description = st.text_input('', 'Rareté des employés', key="problem_description_lean_canvas", label_visibility="collapsed")
        
        with col3:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["solution_description"]}</div>', unsafe_allow_html=True)
            solution_description = st.text_input('', 'Automatisation', key="solution_description_lean_canvas", label_visibility="collapsed")
        
        col4 = st.columns([1])
        with col4[0]:
            confirm_button = st.button(lang_texts["confirm"], key="confirm_problem_solution_button")

        if confirm_button:
            st.session_state.industry_name = industry_name
            st.session_state.problem_description = problem_description
            st.session_state.solution_description = solution_description
            st.session_state.confirmed = True

    if st.session_state.confirmed:
        st.markdown(f'<h2 class="custom-title">{lang_texts["confirm_problem_solution"]}</h2>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        
        with col5:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["problem"]}</div>', unsafe_allow_html=True)
            detailed_problem_description = st.text_area('', st.session_state.problem_description, key="detailed_problem_description_lean_canvas")
        
        with col6:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["solution"]}</div>', unsafe_allow_html=True)
            detailed_solution_description = st.text_area('', st.session_state.solution_description, key="detailed_solution_description_lean_canvas")

        col7 = st.columns([1])
        with col7[0]:
            generate_button = st.button(lang_texts["submit"], key="generate_lean_canvas_button")

        if generate_button:
            if not api_key or not st.session_state.industry_name or not detailed_problem_description or not detailed_solution_description:
                st.warning(f"{lang_texts['api_key']}, {lang_texts['industry']}, {lang_texts['problem']} et {lang_texts['solution']}")
            else:
                try:
                    with st.spinner(lang_texts["result"]):
                        agent = LeanCanvas(api_key, temperature, st.session_state.industry_name, detailed_problem_description, detailed_solution_description, language, year=2024, model=model)
                        lean_canvas = agent.execute()

                        if isinstance(lean_canvas, str):
                            st.markdown(f"**{lang_texts['problem_description']}**: {detailed_problem_description}")
                            st.markdown(f"**{lang_texts['solution_description']}**: {detailed_solution_description}")
                            st.markdown(lean_canvas, unsafe_allow_html=True)
                            st.markdown("<br><br><br>", unsafe_allow_html=True)
                        else:
                            st.error("Lean Canvas généré n'est pas sous forme de texte.")
                    
                except Exception as e:
                    st.error(f"Une erreur est survenue lors de la génération du Lean Canvas pour l'industrie '{st.session_state.industry_name}' avec la solution '{detailed_solution_description}' : {str(e)}")

