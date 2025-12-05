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
        data_str = student_data.head(50).to_string() # Limit to 50 for speed
        return f"""Analyze these students. For each student, provide a mini-profile using this EXACT Markdown format:

### Student Name
* **Performance**: [Summary]
* **Strength**: [Strength]
* **Weakness**: [Weakness]
* **Action**: [Recommendation]

Data:
{data_str}
"""
    else:
        # Text input
        return f"""Analyze this student text. Use this Markdown format:

### Skills Assessment
* **Communication**: [Analysis]
* **Critical Thinking**: [Analysis]

### Recommendations
* [Point 1]
* [Point 2]

Text: "{student_data[:4000]}"
"""

def _create_comparative_prompt(student_data):
    if isinstance(student_data, pd.DataFrame):
        desc = student_data.describe().to_string()
        return f"""Analyze the class performance based on these statistics. Use Markdown:

### Class Overview
[One paragraph summary]

### Key Statistics
* **Top Subject**: [Subject]
* **Subject Needing Focus**: [Subject]

### Teaching Strategy
* [Strategy 1]
* [Strategy 2]

Statistics:
{desc}
"""
    return "Comparative analysis requires structured data."