import streamlit as st
import openai
import base64
import os
import problems
import solutions
import lean_canvas
import business_canvas
import business_plan
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.WARNING)

st.set_page_config(page_title="AI Marketing Innovation Toolkit", layout="wide", page_icon="uqar.png")

# Apply CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def localize_text(language):
    texts = {
        "English": {
            "title": "AI Marketing Innovation Toolkit",
            "api_key": "Enter your API Key",
            "temperature": "Select the temperature",
            "lang": "Select your language",
            "model": "Select Model",
            "apig": "Generate your own Gemini API key by clicking here",
            "warn": "Please enter your API key",
            "tabs": {
                "t_problem": "Problems",
                "t_solution": "Solutions",
                "t_lean_canvas": "Lean Canvas",
                "t_business_canvas": "Business Ca nvas",
                "t_business_plan": "Business Plan"
            }
        },
        "French": {
            "title": "Boîte à outils du marketing de l'innovation avec l'IA",
            "api_key": "Entrez votre clé API",
            "temperature": "Sélectionnez la température",
            "lang": "Sélectionnez votre langue",
            "model": "Sélectionnez le modèle",
            "apig": "Générez votre propre clé Gemini API en cliquant ici",
            "warn":"Veuillez entrer votre clé API",
            "tabs": {
                "t_problem": "Problèmes",
                "t_solution": "Solutions",
                "t_lean_canvas": "Lean Canvas",
                "t_business_canvas": "Business Canvas",
                "t_business_plan": "Plan d'affaires"
            }
        }
    }
    return texts[language]

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logging.error(f"Error converting image to base64: {str(e)}")
        return None

def main():
    with st.expander("**Paramétres**", expanded=True):
        col1, col2, col3, col4 = st.columns([4, 4, 4, 4])
        
        with col1:
            st.markdown(f'<div class="css-hi6a2p">Langue/Langauge</div>', unsafe_allow_html=True)
            lang = st.selectbox("", ("French", "English"), index=0, key='lang')
            lang_texts = localize_text(lang)
        
        with col2:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["model"]}</div>', unsafe_allow_html=True)
            model = st.selectbox("", ("gemini-1.5-pro-latest", "gemini-1.5-flash"), key='model_gemini')
        
        with col3:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["api_key"]}</div>', unsafe_allow_html=True)
            api_key = st.text_input("", key="api_key", type="password", label_visibility="collapsed")
        
        with col4:
            st.markdown(f'<div class="css-hi6a2p">{lang_texts["temperature"]}</div>', unsafe_allow_html=True)
            temperature = st.slider('', 0.0, 1.0, 0.5, key="temperature_problems", label_visibility="collapsed")
        
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="custom-title">{lang_texts["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f'<div class="css-1d391kg">Laboratoire Limnat, UQAR, Campus Lévis (<a href="https://limnat.ca" target="_blank">https://limnat.ca</a>)</div>', unsafe_allow_html=True)
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        uqar_img_base64 = img_to_base64("uqar.jpg")
        if uqar_img_base64:
            st.markdown(
                f'<a href="https://www.uqar.ca" target="_blank"><img src="data:image/png;base64,{uqar_img_base64}" class="cover-glow" alt="UQAR"></a>',
                unsafe_allow_html=True,
            )
        st.text("")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.text("")
        st.text("")
        with st.container():
            st.markdown(f'<a href="https://ai.google.dev/gemini-api/" id="api_link" class="css-1d391kg">{lang_texts["apig"]}</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
    tab_titles = [lang_texts["tabs"]["t_problem"], 
                  lang_texts["tabs"]["t_solution"], 
                  lang_texts["tabs"]["t_lean_canvas"], 
                  lang_texts["tabs"]["t_business_canvas"],
                  lang_texts["tabs"]["t_business_plan"]]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_titles)
    
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key

        with tab1:
            problems.display_problems(api_key, temperature, lang, model)

        with tab2:
           solutions.display_solutions(api_key, temperature, lang, model)

        with tab3:
            lean_canvas.display_lean_canvas(api_key, temperature, lang, model)
             
        with tab4:
            business_canvas.display_business_canvas(api_key, temperature, lang, model)

        with tab5:
            business_plan.display_business_plan(api_key, temperature, lang, model)

    else:
        st.warning(lang_texts["warn"])

if __name__ == '__main__':
    main()