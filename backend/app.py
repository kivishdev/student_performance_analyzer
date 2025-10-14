import os
import sys
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import custom modules
from modules.data_extractor import read_data
from modules.gemini_analyzer import initialize_gemini, _create_analysis_prompt, _create_comparative_prompt

# --- Flask App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(backend_path, 'data')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- API Endpoints ---

@app.route('/')
def index():
    """Serves the main single-page application."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """API endpoint for file and text analysis."""
    model = initialize_gemini()
    if not model:
        return jsonify({"error": "Could not initialize Gemini API. Check API key."}), 500

    file = request.files.get('file')
    text_input = request.form.get('text_input')
    # --- FIX: Read the analysis_type from the form ---
    analysis_type = int(request.form.get('analysis_type', 3)) # Default to 3
    results = {}

    try:
        data_source = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            data_source = read_data(file_path)
            if data_source is None:
                return jsonify({'error': 'Could not read or process the uploaded file.'}), 400
        elif text_input:
            data_source = text_input
        else:
            return jsonify({'error': 'Please upload a file or enter text to analyze.'}), 400

        # --- FIX: Conditional logic based on analysis_type ---
        if analysis_type in [1, 3]: # Run for 'Individual' or 'Complete'
            standard_prompt = _create_analysis_prompt(data_source)
            results['standard'] = model.generate_content(standard_prompt).text

        if analysis_type in [2, 3]: # Run for 'Comparative' or 'Complete'
            # Comparative analysis is only applicable for structured data (not plain text)
            if not isinstance(data_source, str):
                comparative_prompt = _create_comparative_prompt(data_source)
                results['comparative'] = model.generate_content(comparative_prompt).text
            else:
                # If user asks for comparative on text, provide a message
                if analysis_type == 2:
                    results['comparative'] = "Comparative analysis is not applicable for plain text input."
        
        # Ensure at least one result is present
        if not results:
             return jsonify({'error': 'No analysis was generated for the selected type.'}), 400

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred during AI analysis: {e}"}), 500

@app.route('/api/career-guide', methods=['POST'])
def career_guide():
    """API endpoint for the career guide chatbot."""
    model = initialize_gemini()
    if not model:
        return jsonify({"error": "Could not initialize Gemini API."}), 500
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided.'}), 400
    
    user_message = data['message']

    prompt = f"""You are an expert career counselor and academic advisor.
    Based on the following student's description of their interests, skills, or academic marks, provide thoughtful and encouraging career guidance in clear, well-formatted paragraphs.

    Your response should include:
    1.  **Key Strengths Identification:** Briefly identify the core strengths from the text.
    2.  **Top 3 Career Path Suggestions:** Suggest three distinct career paths that align with these strengths.
    3.  **Detailed Rationale:** For each path, explain *why* it's a good fit.
    4.  **Actionable Next Steps:** Provide 2-3 concrete next steps.

    Student's Input:
    ---
    {user_message}
    ---
    """
    try:
        response = model.generate_content(prompt).text
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred during AI analysis: {e}"}), 500

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)


