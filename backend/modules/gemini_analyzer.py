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
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
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

        prompt = f"""You are an expert educational data analyst conducting academic research on student performance.

IMPORTANT FORMATTING RULES:
- Write in plain text only
- Use bullet points with • symbol for lists
- Use simple numbered lists (1. 2. 3.) where needed
- Do NOT use **, *, __, #, or ``` markdown symbols
- Keep sections clear with line breaks
- Write naturally without special formatting

Your task: Provide a detailed, research-quality performance analysis for each student.

For each student, provide:

Student Name:
• Academic Performance: Brief overview of grades/scores
• Key Strength: One specific area of excellence
• Improvement Area: One actionable recommendation
• Overall Assessment: Brief characterization

Guidelines:
- Be objective and data-driven
- Keep each student analysis to 3-4 points
- Use professional academic language
- Focus on constructive feedback
- Identify patterns and trends

Student Data:{data_note}
---
{data_string}
---

Provide individual analysis for each student listed above. Format cleanly with clear sections."""

    elif isinstance(student_data, str):
        # Limit text length for API
        if len(student_data) > 8000:
            text_data = student_data[:8000] + "\n...(truncated)"
        else:
            text_data = student_data

        prompt = f"""You are an expert literary and academic analyst conducting research on student writing.

IMPORTANT FORMATTING RULES:
- Write in plain text only
- Use bullet points with • symbol for lists
- Do NOT use **, *, __, #, or ``` markdown symbols
- Keep sections clear with line breaks
- Write naturally without special formatting

Your task: Provide a comprehensive analysis of the following student text.

Please analyze:

Content Analysis:
• Key themes and arguments presented
• Main ideas and supporting evidence

Writing Quality:
• Style, clarity, and structure assessment
• Coherence and flow evaluation

Critical Strengths:
• What the student does well
• Notable writing techniques

Areas for Improvement:
• Specific, actionable suggestions
• Developmental feedback

Academic Level:
• Estimated proficiency with justification

Guidelines:
- Be thorough and research-oriented
- Provide evidence-based observations
- Use professional academic language
- Focus on developmental feedback

Student Text:
---
{text_data}
---

Provide your comprehensive analysis above. Write in clean, plain text format."""

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
        
        stats_summary = "Statistical Summary:\n"
        for col in numeric_cols:
            stats_summary += f"• {col}: Mean={student_data[col].mean():.2f}, "
            stats_summary += f"Median={student_data[col].median():.2f}, "
            stats_summary += f"Std={student_data[col].std():.2f}\n"

        data_string = student_data.to_string()

        prompt = f"""You are an expert educational researcher conducting class-wide performance analysis.

IMPORTANT FORMATTING RULES:
- Write in plain text only
- Use bullet points with • symbol for lists
- Use numbered lists (1. 2. 3.) for ordered items
- Do NOT use **, *, __, #, or ``` markdown symbols
- Keep sections clear with line breaks
- Write naturally without special formatting

Your task: Provide a comprehensive comparative analysis of this student cohort for research purposes.

{stats_summary}

Full Dataset:
---
{data_string}
---

Please provide:

CLASS OVERVIEW:
• Overall performance trends
• Distribution of achievement levels
• General observations

STATISTICAL INSIGHTS:
• Key metrics analysis
• Performance patterns observed
• Notable outliers or cases

COMPARATIVE ANALYSIS:
• High performers characteristics
• Students needing support
• Subject-wise variations
• Performance correlations

RESEARCH FINDINGS:
• Significant observations
• Potential factors affecting performance
• Patterns worth investigating

RECOMMENDATIONS:
• Class-level interventions suggested
• Differentiation strategies
• Priority areas requiring attention

Provide a thorough, research-quality analysis suitable for academic reporting. Use clean, plain text formatting."""

    else:
        prompt = f"""You are an expert educational researcher analyzing student writing samples.

IMPORTANT FORMATTING RULES:
- Write in plain text only
- Use bullet points with • symbol for lists
- Do NOT use **, *, __, #, or ``` markdown symbols
- Write naturally without special formatting

Student Text Length: {len(student_data)} characters

Provide a meta-analysis suitable for research:

CONTENT COMPLEXITY:
• Vocabulary level assessment
• Sentence structure analysis
• Argumentation depth

WRITING MATURITY:
• Indicators of academic development
• Sophistication markers

RESEARCH POTENTIAL:
• Topics for further exploration
• Themes worth investigating

BENCHMARK ASSESSMENT:
• Comparison to typical student writing
• Grade level appropriateness

PEDAGOGICAL IMPLICATIONS:
• What this reveals about student learning
• Teaching recommendations

Focus on research-oriented insights. Use clean, plain text formatting."""

    return prompt