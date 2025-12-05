import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import custom modules
from modules.data_extractor import read_data, get_chart_data
from modules.gemini_analyzer import initialize_gemini, analyze_student_data, generate_comparative_analysis

# --- Flask App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(backend_path, 'data')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    analysis_type = int(request.form.get('analysis_type', 3))
    results = {}
    chart_data = None

    try:
        data_source = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            data_source = read_data(file_path)
            
            # Extract chart data if it's a dataframe
            if data_source is not None:
                chart_data = get_chart_data(data_source)
                
            if data_source is None:
                return jsonify({'error': 'Could not read or process the uploaded file.'}), 400
        elif text_input:
            data_source = text_input
        else:
            return jsonify({'error': 'Please upload a file or enter text to analyze.'}), 400

        # --- Analysis Logic ---
        if analysis_type in [1, 3]: # Individual or Complete
            # Use the module function which already handles prompts
            results['standard'] = analyze_student_data(data_source)

        if analysis_type in [2, 3]: # Comparative or Complete
            if not isinstance(data_source, str):
                results['comparative'] = generate_comparative_analysis(data_source)
            elif analysis_type == 2:
                results['comparative'] = "Comparative analysis is not applicable for plain text input."
        
        if not results:
             return jsonify({'error': 'No analysis was generated.'}), 400

        # Return results AND chart data
        return jsonify({"text_results": results, "chart_data": chart_data}), 200

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

    prompt = f"""You are an expert career counselor.
    Provide a helpful, encouraging response to this student inquiry.
    Keep it concise (under 150 words) but actionable.
    
    Student: "{user_message}"
    """
    try:
        response = model.generate_content(prompt).text
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)