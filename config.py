# config.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai

# Load environment variables from .env file (for local development)
# This should be called at the very top to ensure variables are loaded
# before any attempts to access them.
load_dotenv()

def initialize_gemini_model():
    """
    Initializes the Gemini model using API key from environment variables or Streamlit secrets.
    Prioritizes environment variables (e.g., from .env) for local development.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    # If not found in environment variables (e.g., when deployed on Streamlit Cloud
    # where secrets are exposed via st.secrets), try st.secrets.
    if not api_key:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key or api_key == "YOUR_GEMINI_API_KEY": # Check for placeholder too
        st.error("Gemini API Key not found. Please set it in a `.env` file (for local development) or in `.streamlit/secrets.toml` (for Streamlit Cloud deployment).")
        st.stop() # Stop the app if API key is missing

    try:
        # Configure the genai library directly for general use (e.g., for direct calls if needed)
        genai.configure(api_key=api_key)

        # Initialize LangChain's ChatGoogleGenerativeAI model
        # Using gemini-2.0-flash for faster responses, and a temperature for creativity
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=api_key)
        return llm
    except Exception as e:
        st.error(f"Failed to initialize Gemini model. Please check your API key and internet connection. Error: {e}")
        st.stop() # Stop the app if the model can't be initialized

# Initialize the LLM once when the app starts
llm = initialize_gemini_model()