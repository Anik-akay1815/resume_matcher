import streamlit as st
import PyPDF2
import re
import nltk
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Resume vs Job matcher",
    page_icon="",
    layout="centered"
)

st.title("Resume vs Job description matcher")
st.markdown("""
Upload your resume and paste a job description.
Get your **ATS match score**, **matched skills**, and **missing skills**
instantly.
""")
st.markdown("---")

with st.sidebar:
    st.title("How to use")
    st.markdown("""
    1. Upload your resume PDF
    2. Paste the job description
    3. Click Analyze Match
    4. Review score and skill gaps
    5. Update your resume accordingly
    """)
st.markdown("---")
st.caption("Built with Python + Streamlit + NLP")

skills_db = [
"python", "java", "javascript", "sql", "react", "node",
"machine learning", "deep learning", "nlp", "docker",
"kubernetes", "aws", "azure", "git", "linux", "flask",
"django", "tensorflow", "pytorch", "pandas", "numpy",
"rest api", "mongodb", "postgresql", "data structures",
"algorithms", "system design", "agile", "ci/cd",
]

#TEXT EXTRACTION FROM PDF
def extract_text(uploaded_file):
    text = " "
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
        return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    stop_words = set(stopwords.words("english"))
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def get_match_score(resume_text, jd_text):
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)
    
    Vectorizer = TfidfVectorizer()
    
    vectors = Vectorizer.fit_transform([clean_resume, clean_jd])
    score = cosine_similarity(vectors[0],vectors[1])[0][0]
    
    return round(score*100, 2)

def extract_skills(text, skills_db):
    text_lower =  text.lower()
    found= []
    for skill in skills_db:
        if skill in text_lower:
            found.append(skill)
            return found

def get_skill_gap(resume_text, jd_text):
    resume_skills = extract_skills(resume_text, skills_db)
    jd_skills = extract_skills(jd_text, skills_db)
    
    matched =[s for s in jd_skills if s in resume_skills]
    missing =[s for s in jd_skills if s not in resume_skills]
    
    return matched, missing


#UI......
st.title("Resume vs JD Matcher")
st.subheader("Step-1: Upload your resume")
resume_text = ""
uploaded_file = st.file_uploader("Upload Resume (PDF only)", type="pdf")

if uploaded_file is not None:
    resume_text = extract_text(uploaded_file)
    st.success("PDF uploaded successfully...")
    with st.expander("See extracted resume text"):
        st.write(resume_text)
        
#JOB DESCRIPTION......
st.subheader("Step-2: Paste Job Description")
jd_text = st.text_area("Paste the full job description here", height=200)

if jd_text:
    st.success("Job description recieved")

#Confirm both are ready
if resume_text and jd_text:
    st.info("Both inputs recieved. Next step: Analyze!")

if resume_text and jd_text:
    st.markdown("----")

if st.button("Analyze Match"):
    score = get_match_score(resume_text, jd_text)
    matched, missing = get_skill_gap(resume_text, jd_text)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Match Score", f"{score}%")
    m2.metric("Matched Skills", len(matched))
    m3.metric("Missing Skills", len(missing))

    with st.spinner("Analyzing..."):
        score = get_match_score(resume_text, jd_text)
        st.subheader("Your Match score:")

    if score >=70:
        st.success(f"Match Score: {score}% — Strong Match")
    elif score >= 45:
        st.warning(f"Match Score: {score}% — Moderate Match")
    else:
        st.error(f"Match Score: {score}% — Weak Match")

    st.progress(int(score))
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Matcher skills:")
        for skill in matched:
            st.success(f"{skill}")
    with col2:
        st.subheader("Mising skills:")
        for skill in missing:
            st.error(f"{skill}")
            
    if missing:
        st.markdown("---")
        st.subheader("How to improve your resume")
        tips =[f"Add a skill section listing:{", ".join(missing[:3])}",
        "Tailor you project descirption to mention missing keywords",
        "Take a short course on the most critical missing skill",
        "Mirror the exact wording from the JD in your resume",]
        for i,tips in enumerate(tips,1):
            st.info(f"{i},{tips}")