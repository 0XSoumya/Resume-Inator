# ai_utils.py
import streamlit as st
from langchain_core.messages import HumanMessage
from config import llm # Import the initialized LLM from config.py

def generate_content_with_ai(prompt_text):
    """
    Generates content using the LangChain LLM based on the given prompt.
    Includes error handling and a loading spinner.
    """
    try:
        with st.spinner("Generating content with AI..."):
            # Use LangChain's invoke method with a HumanMessage
            response = llm.invoke([HumanMessage(content=prompt_text)])
            return response.content
    except Exception as e:
        st.error(f"Error calling AI: {e}. Please check your API key and try again.")
        return "Error generating content."

def generate_summary(raw_summary_input, name, profession):
    """Generates a professional summary using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw input about {name} ({profession}),
    write a concise, impactful, and professional resume summary (3-5 sentences).
    Focus on achievements, key skills, and career goals.

    Raw input:
    {raw_summary_input}

    Professional Summary:
    """
    return generate_content_with_ai(prompt)

def generate_experience(raw_experience_input, name):
    """Formats and enhances work experience entries using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw work experience details for {name},
    format each entry professionally with bullet points highlighting achievements and responsibilities using action verbs.
    Include company, title, location, and dates.

    Raw experience input:
    {raw_experience_input}

    Formatted Work Experience:
    """
    return generate_content_with_ai(prompt)

def generate_education(raw_education_input, name):
    """Formats and enhances education entries using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw education details for {name},
    format each entry professionally. Include degree, major, institution, location, and graduation date (or expected date).
    Add relevant coursework or academic achievements if provided.

    Raw education input:
    {raw_education_input}

    Formatted Education:
    """
    return generate_content_with_ai(prompt)

def generate_skills(raw_skills_input, name):
    """Categorizes and formats skills using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw skills for {name},
    categorize them (e.g., Programming Languages, Tools, Soft Skills, etc.) and present them concisely.
    Use bullet points or comma-separated lists within categories.

    Raw skills input:
    {raw_skills_input}

    Formatted Skills:
    """
    return generate_content_with_ai(prompt)