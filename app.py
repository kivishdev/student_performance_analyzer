import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import traceback

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import custom modules
from modules.data_extractor import read_data, get_chart_data
from modules.gemini_analyzer import initialize_gemini, analyze_student_data, generate_comparative_analysis, analyze_resume

# --- Flask App Configuration ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(backend_path, 'data')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        model = initialize_gemini()
        if not model:
            return jsonify({"error": "Could not initialize Gemini API. Check API key."}), 500

        file = request.files.get('file')
        text_input = request.form.get('text_input')
        
        try:
            analysis_type = int(request.form.get('analysis_type', 3))
        except ValueError:
            analysis_type = 3
            
        results = {}
        chart_data = None
        data_source = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            data_source = read_data(file_path)
            
            if data_source is None:
                return jsonify({'error': 'Could not process file. Valid formats: CSV, Excel, PDF, Text.'}), 400
            
            # Extract chart data if it's a dataframe (CSV/Excel)
            if not isinstance(data_source, str) and analysis_type != 4:
                chart_data = get_chart_data(data_source)
                
        elif text_input:
            data_source = text_input
        else:
            return jsonify({'error': 'Please upload a file or enter text to analyze.'}), 400

        # --- Analysis Logic ---
        # Mode 4 is specifically for Resume/CV
        if analysis_type == 4:
            if not isinstance(data_source, str):
                 # Convert dataframe to string if someone uploaded excel as resume
                 data_source = data_source.to_string()
            results['resume'] = analyze_resume(data_source)
        else:
            # Modes 1, 2, 3
            if analysis_type in [1, 3]: 
                results['standard'] = analyze_student_data(data_source)

            if analysis_type in [2, 3]: 
                if not isinstance(data_source, str):
                    results['comparative'] = generate_comparative_analysis(data_source)
                elif analysis_type == 2:
                    results['comparative'] = "Comparative analysis requires structured data (CSV/Excel). For PDF/Text, please use Individual or Resume mode."
        
        if not results:
             return jsonify({'error': 'No analysis was generated.'}), 400

        return jsonify({"text_results": results, "chart_data": chart_data}), 200

    except Exception as e:
        print(f"Error in analyze_data: {e}")
        traceback.print_exc()
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

@app.route('/api/career-guide', methods=['POST'])
def career_guide():
    try:
        model = initialize_gemini()
        if not model: return jsonify({"error": "API Key missing."}), 500
        
        data = request.get_json()
        if not data: return jsonify({"error": "Invalid request"}), 400

        msg = data.get('message', '')
        mode = data.get('mode', 'chat')

        if not msg: return jsonify({"error": "Message is empty"}), 400

        if mode == 'roadmap':
            prompt = f"""Create a career roadmap for: "{msg}".
            Format as Markdown:
            ### 🎯 Phase 1: Start
            * [Step]
            ### 🚀 Phase 2: Grow
            * [Step]
            ### 🏆 Phase 3: Master
            * [Step]
            """
        else:
            prompt = f"""You are a helpful career counselor. 
            User says: "{msg}". 
            Reply encouragingly in under 100 words."""

        response = model.generate_content(prompt).text
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"Career API Error: {e}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)