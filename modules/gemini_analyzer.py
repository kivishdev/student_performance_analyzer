import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def initialize_gemini():
    """
    Initialize and configure the Gemini API.
    
    Returns:
        genai.GenerativeModel: Configured model instance or None if failed
    """
    try:
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in .env file")
            print("   Please create a .env file with: GOOGLE_API_KEY=your_key_here")
            return None

        genai.configure(api_key=api_key)
        
        # Use gemini-2.0-flash-exp or gemini-1.5-pro as alternatives
        model = genai.GenerativeModel('gemini-2.0-flash-001')
        logging.info("Gemini API initialized successfully")
        return model
    except Exception as e:
        logging.error(f"Gemini initialization error: {e}")
        print(f"❌ Error initializing Gemini API: {e}")
        return None

def analyze_student_data(student_data):
    """
    Analyze student data using Gemini AI with enhanced prompts.

    Args:
        student_data (pd.DataFrame or str): Cleaned data from file

    Returns:
        str: AI-generated analysis or error message
    """
    model = initialize_gemini()
    if not model:
        return "Error: Could not initialize Gemini API"

    try:
        prompt = _create_analysis_prompt(student_data)
        
        if not prompt:
            return "Error: Could not create analysis prompt"

        # Generate content with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'top_p': 0.95,
                        'top_k': 40,
                        'max_output_tokens': 2048,
                    }
                )
                
                return response.text
                
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    logging.warning(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise e

    except Exception as e:
        logging.error(f"Analysis error: {e}")
        return f"Error during AI analysis: {str(e)}"

def generate_comparative_analysis(student_data):
    """
    Generate class-wide comparative analysis and statistics.

    Args:
        student_data (pd.DataFrame or str): Student data

    Returns:
        str: Comparative analysis or error message
    """
    model = initialize_gemini()
    if not model:
        return "Error: Could not initialize Gemini API"

    try:
        prompt = _create_comparative_prompt(student_data)
        
        if not prompt:
            return "Error: Could not create comparative analysis prompt"

        # Generate content with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.5,
                        'top_p': 0.95,
                        'top_k': 40,
                        'max_output_tokens': 2048,
                    }
                )
                
                return response.text
                
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    logging.warning(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(RETRY_DELAY)
                else:
                    raise e

    except Exception as e:
        logging.error(f"Comparative analysis error: {e}")
        return f"Error during comparative analysis: {str(e)}"

def _create_analysis_prompt(student_data):
    """
    Create a tailored prompt based on data type.
    
    Args:
        student_data: DataFrame or string data
        
    Returns:
        str: Formatted prompt for Gemini
    """
    if isinstance(student_data, pd.DataFrame):
        # Limit data size for API
        if len(student_data) > 100:
            data_string = student_data.head(100).to_string()
            data_note = f"\n(Note: Showing first 100 of {len(student_data)} students)"
        else:
            data_string = student_data.to_string()
            data_note = ""

        prompt = f"""Analyze each student's performance. For EACH student provide EXACTLY 4 points:

1. Current Performance: One sentence about grades/scores
2. Strongest Subject: One specific strength
3. Needs Improvement: One specific weakness  
4. Action: One clear recommendation

Format: No **, *, #, or ``` symbols. Use bullet points (•).
Be direct and concise - 2-3 sentences per student maximum.

Data:{data_note}
{data_string}

Start analyzing now."""

    elif isinstance(student_data, str):
        # Limit text length for API
        if len(student_data) > 8000:
            text_data = student_data[:8000] + "\n...(truncated)"
        else:
            text_data = student_data

        prompt = f"""Based on this student's writing, analyze their academic abilities and future potential:

1. STUDENT SKILLS (3 points):
   • Communication ability level
   • Critical thinking capability
   • Academic readiness

2. LEARNING STRENGTHS (2 points):
   • Best learning traits shown
   • Natural talents observed

3. AREAS TO DEVELOP (2 points):
   • Skills needing practice
   • Knowledge gaps to fill

4. CAREER POTENTIAL (3 points):
   • Suitable career paths based on writing
   • Subject areas to explore
   • Academic majors to consider

5. FUTURE GUIDANCE (2 points):
   • Next steps for improvement
   • Recommended focus areas

Format: Plain text, bullet points (•), no ** or *.
Each point ONE sentence. Focus on the STUDENT, not just the text.
Total: 250 words max.

Student's Writing:
{text_data}

Analyze the student now."""

    else:
        logging.error("Invalid data type for analysis")
        return None

    return prompt

def _create_comparative_prompt(student_data):
    """
    Create prompt for class-wide comparative analysis.
    
    Args:
        student_data: DataFrame or string data
        
    Returns:
        str: Formatted prompt for comparative analysis
    """
    if isinstance(student_data, pd.DataFrame):
        # Calculate basic statistics
        numeric_cols = student_data.select_dtypes(include=['number']).columns
        
        stats_summary = "Stats:\n"
        for col in numeric_cols:
            stats_summary += f"• {col}: Mean={student_data[col].mean():.2f}, "
            stats_summary += f"Median={student_data[col].median():.2f}, "
            stats_summary += f"Std={student_data[col].std():.2f}\n"

        data_string = student_data.to_string()

        prompt = f"""Analyze this class data. Provide EXACTLY these 5 sections:

1. CLASS OVERVIEW (3 bullets):
   • Overall performance level
   • Achievement distribution
   • Key observation

2. TOP PERFORMERS (2 bullets):
   • Who are they
   • Common traits

3. STRUGGLING STUDENTS (2 bullets):
   • Who needs help
   • Common challenges

4. PATTERNS (3 bullets):
   • Subject-wise trends
   • Performance correlations
   • Notable outliers

5. ACTIONS (3 bullets):
   • Priority interventions
   • Teaching strategies
   • Focus areas

Format: Plain text, bullet points (•), no ** or *.
Keep each point to ONE sentence. Total: 300 words max.

{stats_summary}

Data:
{data_string}

Start analysis now."""

    else:
        prompt = f"""Analyze the student behind this writing sample:

1. STUDENT PROFILE:
   • Academic maturity level
   • Learning style indicators
   • Intellectual curiosity shown

2. ACADEMIC STRENGTHS:
   • Subject areas they'd excel in
   • Natural abilities demonstrated

3. SKILL GAPS:
   • Areas needing development
   • Learning challenges observed

4. CAREER DIRECTIONS:
   • Suitable career fields
   • Educational paths to consider
   • Industry sectors matching skills

5. DEVELOPMENT PLAN:
   • Short-term goals (next 6 months)
   • Long-term focus areas
   • Resources to use

Format: Plain text, bullet points (•), no ** or *.
Focus on the STUDENT'S potential and future, not just the text.
250 words max.

Text length: {len(student_data)} characters

Analyze the student now."""

    return prompt