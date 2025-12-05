import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
MAX_RETRIES = 3
RETRY_DELAY = 2

def initialize_gemini():
    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash-001')
    except Exception as e:
        logging.error(f"Gemini initialization error: {e}")
        return None

def analyze_student_data(student_data):
    model = initialize_gemini()
    if not model: return "Error: API Key missing."
    try:
        prompt = _create_analysis_prompt(student_data)
        return _generate_with_retry(model, prompt)
    except Exception as e:
        return f"Error: {str(e)}"

def generate_comparative_analysis(student_data):
    model = initialize_gemini()
    if not model: return "Error: API Key missing."
    try:
        prompt = _create_comparative_prompt(student_data)
        return _generate_with_retry(model, prompt)
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_resume(resume_text):
    """Specific function for analyzing resumes."""
    model = initialize_gemini()
    if not model: return "Error: API Key missing."
    try:
        # Truncate if too long
        text = str(resume_text)[:15000]
        prompt = f"""You are an expert Career Coach and HR Manager. Analyze this resume/CV.
        
        Please provide the output in the following Markdown format:

        ### 📋 Resume Summary
        [2-3 sentence professional summary of the candidate]

        ### ⭐ Key Strengths
        * **Skill 1**: [Detail]
        * **Skill 2**: [Detail]
        * **Experience**: [Highlight]

        ### 🚩 Areas for Improvement
        * [Weakness or formatting issue]
        * [Missing keyword or skill]

        ### 💼 Career Fit
        * **Best Roles**: [Role 1], [Role 2]
        * **Industry**: [Industry Name]

        Resume Content:
        "{text}"
        """
        return _generate_with_retry(model, prompt)
    except Exception as e:
        return f"Error analyzing resume: {str(e)}"

def _generate_with_retry(model, prompt):
    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                raise e

def _create_analysis_prompt(student_data):
    if isinstance(student_data, pd.DataFrame):
        data_str = student_data.head(50).to_string()
        return f"""Analyze these students. Markdown format:
### Student Name
* **Performance**: [Summary]
* **Action**: [Recommendation]

Data:
{data_str}
"""
    else:
        text_content = str(student_data)[:10000]
        return f"""Analyze this academic text/essay. Markdown format:
### Summary
[Overview]
### Assessment
* [Point 1]
### Feedback
* [Point 2]

Content:
"{text_content}"
"""

def _create_comparative_prompt(student_data):
    if isinstance(student_data, pd.DataFrame):
        desc = student_data.describe().to_string()
        return f"""Analyze class stats. Markdown format:
### Class Overview
[Summary]
### Key Stats
* **Top**: [Subject]
### Strategy
* [Tip]

Stats:
{desc}
"""
    return "Comparative analysis requires structured data."