import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Optional

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def localize_text(language):
    texts = {
        "English": {
            "title": "Business Canvas",
            "input_details": "Enter the details below:",
            "industry": "Industry:",
            "job_to_be_done": "Describe the essence of your business:",
            "customer_description": "Describe your target customers:",
            "submit": "Submit",
            "result_vp": "Value Proposition Canvas",
            "result_bc": "Business Model Canvas",
            "api_key": "Enter your Google API Key",
            "temperature": "Select the temperature",
            "error": "An error occurred while generating the Business Canvas"
        },
        "French": {
            "title": "Canvas du modèle d'affaires",
            "input_details": "Entrez les détails ci-dessous :",
            "industry": "Industrie :",
            "job_to_be_done": "Décrivez l'essence de votre business :",
            "customer_description": "Décrivez votre clientèle cible :",
            "submit": "Soumettre",
            "result_vp": "Canvas de Proposition de Valeur",
            "result_bc": "Business Model Canvas",
            "api_key": "Entrez votre clé API Google",
            "temperature": "Sélectionnez la température",
            "error": "Une erreur est survenue lors de la génération du Canvas du modèle d'affaires"
        }
    }
    return texts[language]

class BusinessCanvas:
    def __init__(self, google_api_key, google_temperature, industry_name, job_to_be_done, customer_description, language):
        self.gpt_model = ChatGoogleGenerativeAI(api_key=google_api_key, model="gemini-1.5-flash")
        self.google_api_key = google_api_key
        self.google_temperature = google_temperature
        self.industry_name = industry_name
        self.job_to_be_done = job_to_be_done
        self.customer_description = customer_description
        self.language = language

    def call_google_chat(self, prompt):
        response = self.gpt_model.invoke(prompt)
        return response.content

    def format_markdown_table(self, content: str) -> str:
        formatted_content = content.replace('* ', '<br>* ')
        return formatted_content

    def generate_value_proposition_canvas(self):
        prompt = f"""
            Imagine you are the founder of a new startup in the {self.industry_name} industry. Your target customers are {self.customer_description} who are looking for a solution to the following problem: {self.job_to_be_done}.
            Your goal is to create a value proposition that clearly communicates the unique benefits and value your product or service provides to your target customers. Please respond only in the {self.language} language. Present the value proposition canvas in a markdown table with the following sections: 'Customer Jobs', 'Pains', 'Gains', 'Products & Services', 'Pain Relievers', and 'Gain Creators'.
        """
        response = self.call_google_chat(prompt)
        return self.format_markdown_table(response)

    def generate_business_model_canvas(self, value_proposition_canvas):
        prompt = f"""
            Act as a business consultant from a top management company.
            I want you to generate a Business Model Canvas for a company in the {self.industry_name} industry that delivers the value proposition: {value_proposition_canvas} to {self.customer_description}. You should complete the business canvas with the following components: 'Key Activities', 'Key Resources', 'Key Partners', 'Customer Relationships', 'Channels', 'Customer Segments', 'Cost Structure', and 'Revenue Streams'. Please respond only in the {self.language} language. Present the business canvas in a markdown table.
        """
        response = self.call_google_chat(prompt)
        return self.format_markdown_table(response)

    def execute(self):
        value_proposition_canvas = self.generate_value_proposition_canvas()
        business_model_canvas = self.generate_business_model_canvas(value_proposition_canvas)
        return value_proposition_canvas, business_model_canvas

def display_business_canvas(api_key, temperature, lang, model):
    load_css('style.css')

    lang_texts = localize_text(lang)
    
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["industry"]}</div>', unsafe_allow_html=True)
        industry_name = st.text_input('', 'Bijouteries', key="industry_name_business_canvas", label_visibility="collapsed")
    
    with col2:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["job_to_be_done"]}</div>', unsafe_allow_html=True)
        job_to_be_done = st.text_input('', 'Vente des bijoux rares', key="job_to_be_done", label_visibility="collapsed")
    
    with col3:
        st.markdown(f'<div class="css-hi6a2p">{lang_texts["customer_description"]}</div>', unsafe_allow_html=True)
        customer_description = st.text_input('', 'Consommateurs aisés', key="customer_description", label_visibility="collapsed")
    
    col4 = st.columns([1])
    with col4[0]:
        generate_button = st.button(lang_texts["submit"], key="generate_button_business_canvas")

    if generate_button:
        if not api_key or not industry_name or not job_to_be_done or not customer_description:
            st.warning(f"{lang_texts['api_key']}, {lang_texts['industry']}, {lang_texts['job_to_be_done']} et {lang_texts['customer_description']}")
        else:
            try:
                with st.spinner(lang_texts["result_vp"]):
                    agent = BusinessCanvas(api_key, temperature, industry_name, job_to_be_done, customer_description, lang)
                    value_proposition_canvas, business_model_canvas = agent.execute()
                    
                    st.markdown(f'**{lang_texts["result_vp"]}**')
                    st.markdown(value_proposition_canvas, unsafe_allow_html=True)
                    st.markdown('<br><br><br>', unsafe_allow_html=True)

                    with st.spinner(lang_texts["result_bc"]):
                        st.markdown(f'**{lang_texts["result_bc"]}**')
                        st.markdown(business_model_canvas, unsafe_allow_html=True)
                        st.markdown('<br><br>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"{lang_texts['error']} : {str(e)}")
