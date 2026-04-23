"""Flask web app for Semester Success Planner"""
import os
import tempfile
from flask import Flask, render_template, request, jsonify
from planner import SemesterPlanner
from evaluator import run_evaluation_silent
from utils import is_demo_mode

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

planner = None


def initialize_planner():
    """Initialize planner with demo mode if needed"""
    global planner
    if planner is None:
        if os.getenv("DEMO_MODE"):
            os.environ["DEMO_MODE"] = "true"
        planner = SemesterPlanner()


@app.route('/')
def index():
    """Render home page"""
    initialize_planner()
    return render_template('index.html', demo_mode=is_demo_mode())


@app.route('/api/plan', methods=['POST'])
def generate_plan():
    """Generate a plan from user prompt and optional syllabus"""
    try:
        initialize_planner()
        
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Please provide a planning prompt'}), 400
        
        # Handle optional syllabus upload
        syllabus_text = ""
        if 'syllabus' in request.files:
            file = request.files['syllabus']
            if file and file.filename:
                try:
                    if file.filename.endswith('.pdf'):
                        # For PDF, we'd need pdf2image library - for now accept as text
                        syllabus_text = file.read().decode('utf-8', errors='ignore')[:2000]
                    else:
                        syllabus_text = file.read().decode('utf-8', errors='ignore')[:2000]
                except Exception as e:
                    return jsonify({'error': f'Could not read syllabus: {str(e)}'}), 400
        
        # Enhance prompt with syllabus context if provided
        if syllabus_text:
            prompt = f"{prompt}\n\n[Student's Syllabus Context]\n{syllabus_text}"
        
        result = planner.generate_plan(prompt)
        
        return jsonify({
            'plan': result['plan_text'],
            'review': result['review_text'],
            'confidence': round(result['confidence'], 2),
            'sources': result['sources']
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error generating plan: {str(e)}'}), 500


@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Run evaluation harness"""
    try:
        initialize_planner()
        results = run_evaluation_silent()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': f'Evaluation failed: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'demo_mode': is_demo_mode()}), 200


if __name__ == '__main__':
    # Enable demo mode if no API key
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["DEMO_MODE"] = "true"
    
    app.run(debug=True, port=5000)
