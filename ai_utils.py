# ai_utils.py
import streamlit as st
from langchain_core.messages import HumanMessage
from config import llm  # Import the initialized LLM from config.py

def generate_content_with_ai(prompt_text):
    """
    Generates content using the LangChain LLM based on the given prompt.
    Includes error handling and a loading spinner.
    """
    try:
        with st.spinner("Generating content with AI..."):
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
    return ONLY the final formatted content directly usable in a resume.

    Do NOT include explanations, suggestions, or commentary.
    Format each entry with bullet points under: Company, Title, Location (optional), and Dates.

    Raw experience input:
    {raw_experience_input}

    Final Resume-Ready Work Experience:
    """
    return generate_content_with_ai(prompt)

def generate_education(raw_education_input, name):
    """Formats and enhances education entries using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw education details for {name},
    format each entry *only for use in a resume*. 

    Return only the formatted output. Do NOT include explanations, rationales, or instructions.
    Include: degree, major, institution, location, graduation date (or expected).

    Raw education input:
    {raw_education_input}

    Final Resume-Ready Education:
    """
    return generate_content_with_ai(prompt)

def generate_skills(raw_skills_input, name):
    """Categorizes and formats skills using AI."""
    prompt = f"""
    You are an expert resume writer. Based on the following raw skills list for {name},
    categorize them into relevant sections (e.g., Programming Languages, Tools, Soft Skills).

    Return only the final resume-ready bullet list. Do NOT include commentary or extra notes.

    Raw skills input:
    {raw_skills_input}

    Final Resume-Ready Skills:
    """
    return generate_content_with_ai(prompt)

def generate_ats_feedback(resume_text, job_description):
    prompt = f"""
    You are an ATS system evaluator.

    Analyze how well this resume matches the job description. Provide:
    1. A score from 0 to 100
    2. A short explanation (2-3 sentences)
    3. A list of missing or suggested keywords (if any)

    --- RESUME ---
    {resume_text}

    --- JOB DESCRIPTION ---
    {job_description}

    ATS Score and Feedback:
    """
    return generate_content_with_ai(prompt)
