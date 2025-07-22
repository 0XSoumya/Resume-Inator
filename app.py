# app.py
import streamlit as st
from ai_utils import generate_summary, generate_experience, generate_education, generate_skills, generate_ats_feedback
from pdf_utils import create_resume_pdf  # ✅ use new ReportLab-based version


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

# ---- Clean up AI output ----
def clean_resume_output(text):
    skip_keywords = [
        "Explanation", "suggestion", "note", "Good luck", "Okay", "Reminder", "Consider", "Let me know",
        "Based on your input", "Here's", "I've", "In this section", "You can"
    ]
    lines = text.splitlines()
    return "\n".join(
        line for line in lines
        if not any(skip.lower() in line.lower() for skip in skip_keywords)
    )

# Initialize session state
for section in ['generated_summary', 'generated_experience', 'generated_education', 'generated_skills']:
    if section not in st.session_state:
        st.session_state[section] = ""

# --- Summary Section ---
st.subheader("1. Professional Summary")
raw_summary = st.text_area(
    "Tell me about your career goals, key strengths, and experience:",
    height=100, key="raw_summary_input"
)
if st.button("Generate Summary", key="generate_summary_btn"):
    if raw_summary:
        st.session_state.generated_summary = generate_summary(raw_summary, name, profession)
    else:
        st.warning("Please provide some input for the summary.")
st.write("**AI-Generated Summary:**")
st.text_area("Summary Output", st.session_state.generated_summary, height=150, key="summary_output")

st.markdown("---")

# --- Experience Section ---
st.subheader("2. Work Experience")
raw_experience = st.text_area(
    "List your work experience (company, title, dates, bullet points):",
    height=200, key="raw_experience_input"
)
if st.button("Generate Experience", key="generate_experience_btn"):
    if raw_experience:
        ai_output = generate_experience(raw_experience, name)
        st.session_state.generated_experience = clean_resume_output(ai_output)
    else:
        st.warning("Please provide some input for work experience.")
st.write("**AI-Generated Work Experience:**")
st.text_area("Experience Output", st.session_state.generated_experience, height=250, key="experience_output")

st.markdown("---")

# --- Education Section ---
st.subheader("3. Education")
raw_education = st.text_area(
    "List your educational background (degree, major, institution, date):",
    height=120, key="raw_education_input"
)
if st.button("Generate Education", key="generate_education_btn"):
    if raw_education:
        ai_output = generate_education(raw_education, name)
        st.session_state.generated_education = clean_resume_output(ai_output)
    else:
        st.warning("Please provide some input for education.")
st.write("**AI-Generated Education:**")
st.text_area("Education Output", st.session_state.generated_education, height=150, key="education_output")

st.markdown("---")

# --- Skills Section ---
st.subheader("4. Skills")
raw_skills = st.text_area(
    "List your skills separated by commas or newlines (e.g., Python, ML, Git):",
    height=100, key="raw_skills_input"
)
if st.button("Generate Skills", key="generate_skills_btn"):
    if raw_skills:
        ai_output = generate_skills(raw_skills, name)
        st.session_state.generated_skills = clean_resume_output(ai_output)
    else:
        st.warning("Please provide some input for skills.")
st.write("**AI-Generated Skills:**")
st.text_area("Skills Output", st.session_state.generated_skills, height=150, key="skills_output")

st.markdown("---")

# --- Download Resume ---
st.subheader("Download Your Resume")

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

if any([resume_data["summary"], resume_data["experience"], resume_data["education"], resume_data["skills"]]):
    pdf_bytes = create_resume_pdf(resume_data)
    st.download_button(
        label="📄 Download Resume as PDF",
        data=pdf_bytes,
        file_name=f"{name.replace(' ', '_')}_Resume.pdf",
        mime="application/pdf"
    )
    st.success("Resume ready for download!")
else:
    st.info("Generate content for at least one section to enable PDF download.")

st.markdown("---")
st.caption("Built with 💼 LangChain + Gemini + Streamlit")

st.subheader("🎯 ATS Score Checker")
st.markdown("Paste a job description below to see how well your resume matches it.")

job_desc = st.text_area("Job Description", height=200)

if st.button("Generate ATS Score"):
    combined_resume = "\n".join([
        resume_data["summary"],
        resume_data["experience"],
        resume_data["education"],
        resume_data["skills"]
    ])
    if job_desc and combined_resume.strip():
        ats_feedback = generate_ats_feedback(combined_resume, job_desc)
        st.markdown("#### 📊 ATS Feedback")
        st.text_area("ATS Output", ats_feedback, height=250)
    else:
        st.warning("Please generate resume content and provide a job description.")
