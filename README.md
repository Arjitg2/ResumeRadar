# ResumeRadar
 # 🧠 Resume Radar – ATS Resume Analyzer using Gemini AI

Resume Radar is an AI-powered tool that evaluates resumes against job descriptions using Google's Gemini 1.5 Pro model. It simulates an Applicant Tracking System (ATS) and an HR Manager to give you precise feedback on how well your resume fits the job role.

---

## 🚀 Features

- 📌 **PDF Resume Upload**: Upload your resume in `.pdf` format.
- 🔍 **ATS Evaluation**: Get a percentage match and missing keywords from the job description.
- 👨‍💼 **HR Review**: See strengths, weaknesses, and an overall evaluation of your resume.
- 💬 **Natural Language Interaction**: Powered by Google Gemini for smart and adaptive analysis.
- 🧾 **JSON Output**: Clean and structured feedback for developers and non-tech users alike.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **AI Model**: Gemini 1.5 Pro via Google Generative AI
- **PDF Parsing**: PyPDF2
- **Environment Management**: python-dotenv

---

## Install Dependencies

pip install -r requirements.txt


---

## Setup .env File

GOOGLE_API_KEY = "your_google_api_key_here"

---

## ⭐ Run the app using

streamlit run resume_radar.py


---
