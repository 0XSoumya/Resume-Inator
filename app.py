# app.py
import streamlit as st
from ai_utils import generate_summary, generate_experience, generate_education, generate_skills
from pdf_utils import create_resume_pdf
# config.py is imported implicitly when ai_utils is imported, ensuring LLM is initialized

st.set_page_config(layout="wide", page_title="AI Resume Builder")

st.title("✨ AI Resume Builder")
st.markdown("""
    Craft a professional resume effortlessly with the power of AI!
    Enter your raw details, let Gemini refine them, and download your polished resume.
""")

st.sidebar.header("Your Details")
st.sidebar.info("Enter your basic information here. This will be used to personalize AI-generated content.")

with st.sidebar:
    name = st.text_input("Full Name", "John Doe")
    profession = st.text_input("Your Profession/Desired Role", "Software Engineer")
    email = st.text_input("Email", "john.doe@example.com")
    phone = st.text_input("Phone", "+1 (123) 456-7890")
    linkedin = st.text_input("LinkedIn Profile URL", "linkedin.com/in/johndoe")

st.header("Resume Sections")

# Initialize session state for generated content
if 'generated_summary' not in st.session_state:
    st.session_state.generated_summary = ""
if 'generated_experience' not in st.session_state:
    st.session_state.generated_experience = ""
if 'generated_education' not in st.session_state:
    st.session_state.generated_education = ""
if 'generated_skills' not in st.session_state:
    st.session_state.generated_skills = ""

# --- Summary Section ---
st.subheader("1. Professional Summary")
raw_summary = st.text_area(
    "Tell me about your career goals, key strengths, and experience (e.g., 'Experienced software engineer with 5 years in web development, skilled in Python and React, seeking to build scalable applications.')",
    height=100,
    key="raw_summary_input"
)
if st.button("Generate Summary", key="generate_summary_btn"):
    if raw_summary:
        st.session_state.generated_summary = generate_summary(raw_summary, name, profession)
    else:
        st.warning("Please provide some input for the summary.")
st.markdown("---")
st.write("**AI-Generated Summary:**")
st.text_area("Summary Output", st.session_state.generated_summary, height=150, key="summary_output")


# --- Experience Section ---
st.subheader("2. Work Experience")
raw_experience = st.text_area(
    "List your work experience. Include company, title, dates, and a few bullet points of your responsibilities and achievements for each role. (e.g., 'Google | Software Engineer | 2020-Present | Developed X, Achieved Y')",
    height=200,
    key="raw_experience_input"
)
if st.button("Generate Experience", key="generate_experience_btn"):
    if raw_experience:
        st.session_state.generated_experience = generate_experience(raw_experience, name)
    else:
        st.warning("Please provide some input for work experience.")
st.markdown("---")
st.write("**AI-Generated Work Experience:**")
st.text_area("Experience Output", st.session_state.generated_experience, height=250, key="experience_output")


# --- Education Section ---
st.subheader("3. Education")
raw_education = st.text_area(
    "List your educational background. Include degree, major, institution, location, and graduation date. (e.g., 'Stanford University | M.S. Computer Science | 2019')",
    height=100,
    key="raw_education_input"
)
if st.button("Generate Education", key="generate_education_btn"):
    if raw_education:
        st.session_state.generated_education = generate_education(raw_education, name)
    else:
        st.warning("Please provide some input for education.")
st.markdown("---")
st.write("**AI-Generated Education:**")
st.text_area("Education Output", st.session_state.generated_education, height=150, key="education_output")


# --- Skills Section ---
st.subheader("4. Skills")
raw_skills = st.text_area(
    "List your skills, separated by commas or new lines. (e.g., 'Python, JavaScript, React, SQL, AWS, Project Management, Communication')",
    height=100,
    key="raw_skills_input"
)
if st.button("Generate Skills", key="generate_skills_btn"):
    if raw_skills:
        st.session_state.generated_skills = generate_skills(raw_skills, name)
    else:
        st.warning("Please provide some input for skills.")
st.markdown("---")
st.write("**AI-Generated Skills:**")
st.text_area("Skills Output", st.session_state.generated_skills, height=150, key="skills_output")


# --- Download Resume ---
st.subheader("Download Your Resume")

# Collect all generated data for PDF
resume_data = {
    "name": name,
    "email": email,
    "phone": phone,
    "linkedin": linkedin,
    "summary": st.session_state.generated_summary,
    "experience": st.session_state.generated_experience,
    "education": st.session_state.generated_education,
    "skills": st.session_state.generated_skills
}

if st.session_state.generated_summary or st.session_state.generated_experience or \
   st.session_state.generated_education or st.session_state.generated_skills:
    pdf_bytes = create_resume_pdf(resume_data)
    st.download_button(
        label="Download Resume as PDF",
        data=pdf_bytes,
        file_name=f"{name.replace(' ', '_')}_Resume.pdf",
        mime="application/pdf"
    )
    st.success("Resume ready for download!")
else:
    st.info("Generate content for at least one section to enable PDF download.")

st.markdown("---")
st.caption("Powered by Gemini API, LangChain, and Streamlit")