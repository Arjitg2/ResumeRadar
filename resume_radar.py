from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf
from google import genai
import json
import re

# Create Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini API response
def get_gemini_response(input_prompt, pdf_content, jd_input):
    # Combine inputs
    input_data = f"{input_prompt}\n\nResume Content:\n{pdf_content}\n\nJob Description:\n{jd_input}"
    
    # Get the response from the model using the new SDK
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=input_data,
        config={
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
    )
    
    # Parse JSON safely
    try:
        parsed_response = json.loads(response.text)
        return parsed_response
    except json.JSONDecodeError:
        st.error("Invalid response format received. Please try again.")
        return None

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    else:
        raise FileNotFoundError("No PDF File Uploaded")

# Prompts
input_prompt1 = """
Hey, act like a highly skilled ATS (Application Tracking System) with expertise in tech fields like software engineering, data science, and big data.
Your task is to evaluate resumes based on a provided job description. 
Provide accurate percentage matching, missing keywords, and a concise profile summary.
Your response should be in this JSON format:
{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}
"""

input_prompt2 = """
You are an experienced Technical HR Manager. Review the provided resume against the given job description.
Share an evaluation highlighting the strengths and weaknesses of the resume in relation to the role.
Your response MUST STRICTLY follow this JSON format without any explanation or additional text:
{"Strengths": "List of strengths", "Weaknesses": "List of weaknesses", "Overall Evaluation": "Your conclusion here"}
Do not include any backticks, markdown, or extra text.
"""

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Inputs
input_text = st.text_area("Paste the Job Description here:", key="jd_input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"], help="Please upload a PDF file")

# Display success message
if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")

# Buttons
submit1 = st.button("Percentage Match")
submit2 = st.button("Tell me about my Resume")

# Process uploaded file
if uploaded_file:
    resume_text = extract_pdf_text(uploaded_file)

    if submit1:
        st.subheader("📊 Resume Match Results")
        with st.spinner('🔍 Analyzing resume against ATS standards...'):
            response = get_gemini_response(input_prompt1, resume_text, input_text)
        
        if response:
            # Extract match percentage
            match_percentage = int(response["JD Match"].replace("%", ""))
            
            # Display match metric prominently
            st.metric(label="🎯 Match Confidence", value=f"{match_percentage}%")
            st.progress(match_percentage / 100)
            
            # Create two columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.error("❌ Missing Keywords")
                if response["MissingKeywords"]:
                    for keyword in response["MissingKeywords"]:
                        st.write(f"• {keyword}")
                else:
                    st.write("✅ No missing keywords detected!")
            
            with col2:
                st.success("✨ Profile Summary")
                st.write(response["Profile Summary"])

    if submit2:
        st.subheader("👔 HR Evaluation")
        with st.spinner('💼 Generating professional evaluation...'):
            response = get_gemini_response(input_prompt2, resume_text, input_text)
        
        if response:
            # Create three sections for evaluation
            st.success("💪 Strengths")
            st.write(response["Strengths"])
            
            st.warning("⚠️ Areas for Improvement")
            st.write(response["Weaknesses"])
            
            st.info("📝 Overall Evaluation")
            st.write(response["Overall Evaluation"])
