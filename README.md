# 🚀 Resume vs Job Description Matcher

An AI-powered Resume Matcher that compares resumes with job descriptions using NLP techniques.

## 🔥 Features
- 📄 Upload Resume (PDF)
- 📝 Paste Job Description
- 📊 Calculates ATS Match Score
- ✅ Shows Matched Skills
- ❌ Shows Missing Skills
- 💡 Provides Improvement Tips

## 🛠 Tech Stack
- Python
- Streamlit
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- NLTK

## ⚙️ How it works
1. Extract text from resume
2. Clean and preprocess text
3. Convert text into vectors using TF-IDF
4. Compute similarity using cosine similarity
5. Display match score and insights

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
