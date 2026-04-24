"""Flask web app for Semester Success Planner"""
import os
import tempfile
import traceback
from flask import Flask, render_template, request, jsonify

# Enable demo mode by default if no API key
if not os.getenv("OPENAI_API_KEY"):
    os.environ["DEMO_MODE"] = "true"
    print("✓ Demo mode enabled (no OpenAI API key detected)")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

planner = None


def initialize_planner():
    """Initialize planner with demo mode if needed"""
    global planner
    if planner is None:
        try:
            print("Initializing planner...")
            from planner import SemesterPlanner
            from utils import is_demo_mode
            planner = SemesterPlanner()
            print("✓ Planner initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing planner: {e}")
            traceback.print_exc()
            raise


@app.route('/')
def index():
    """Render home page"""
    try:
        from utils import is_demo_mode
        return render_template('index.html', demo_mode=is_demo_mode())
    except Exception as e:
        print(f"✗ Error in index route: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Failed to load page: {str(e)}'}), 500


@app.route('/test', methods=['GET'])
def test():
    """Simple test route to check if server is working"""
    from utils import is_demo_mode
    return jsonify({'status': 'ok', 'message': 'Flask server is running!', 'demo_mode': is_demo_mode()}), 200


@app.route('/api/plan', methods=['POST'])
def generate_plan():
    """Generate a plan from user prompt and multiple syllabi"""
    try:
        initialize_planner()
        from evaluator import run_evaluation_silent
        from datetime import datetime
        
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({'error': 'Please provide a planning prompt'}), 400
        
        # Handle multiple syllabus uploads
        syllabi_data = []
        if 'syllabi' in request.files:
            files = request.files.getlist('syllabi')
            for file in files:
                if file and file.filename:
                    try:
                        content = file.read().decode('utf-8', errors='ignore')[:3000]
                        syllabi_data.append({
                            'filename': file.filename,
                            'content': content
                        })
                        print(f"✓ Processed: {file.filename}")
                    except Exception as e:
                        print(f"⚠ Warning: Could not read {file.filename}: {e}")
        
        # Build enhanced prompt with syllabus analysis
        enhanced_prompt = prompt
        if syllabi_data:
            syllabi_text = "\n\n---\n\n".join([
                f"**{s['filename']}**:\n{s['content']}" 
                for s in syllabi_data
            ])
            
            current_date = datetime.now().strftime("%B %d, %Y")
            
            enhanced_prompt = f"""Today is {current_date}. A student needs help planning their semester.

STUDENT REQUEST: {prompt}

{f'They uploaded {len(syllabi_data)} course syllabus/syllabi:' if len(syllabi_data) > 0 else ''}
{syllabi_text if syllabi_text else ''}

IMPORTANT - Follow these steps:
1. **ANALYZE SYLLABI FIRST**: Extract key information:
   - Course names and codes
   - Meeting times/schedule
   - Major assignments, projects, papers (with due dates)
   - Exam dates and types
   - Grading breakdown
   - Prerequisites/dependencies between courses

2. **IDENTIFY PATTERNS**: Look for:
   - When exams cluster together
   - When major projects are due
   - High-workload periods
   - Natural breaks

3. **CREATE COMPREHENSIVE PLAN**: Based on the analysis, provide:
   - Weekly schedule integrating ALL courses
   - Study prep timeline before each exam
   - Assignment deadlines with buffer time
   - Balanced workload distribution
   - Extracurricular activity integration
   - Mental health and wellness checkpoints
   - Conflict resolution (overlapping deadlines)

4. **BE SPECIFIC**: Include actual dates from syllabi, not generic advice

Please provide a detailed, actionable semester plan that shows you understood the syllabi."""
        
        result = planner.generate_plan(enhanced_prompt)
        confidence = round(result['confidence'], 2)
        
        return jsonify({
            'plan': result['plan_text'],
            'review': result['review_text'],
            'confidence': confidence,
            'confidence_explanation': get_confidence_explanation(confidence, len(syllabi_data)),
            'sources': result['sources'],
            'syllabi_processed': len(syllabi_data)
        }), 200
    
    except Exception as e:
        print(f"✗ Error in generate_plan: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Error generating plan: {str(e)}'}), 500


def get_confidence_explanation(confidence: float, syllabi_count: int = 0) -> str:
    """Explain what the confidence score means"""
    base_msg = ""
    
    if syllabi_count > 0:
        base_msg = f"📄 Analyzed {syllabi_count} syllabus/syllabi. "
    
    if confidence >= 0.9:
        return base_msg + "✅ HIGH CONFIDENCE: Plan is comprehensive, grounded in your actual syllabi, and highly actionable."
    elif confidence >= 0.8:
        return base_msg + "✓ GOOD CONFIDENCE: Plan covers main courses and deadlines with solid structure."
    elif confidence >= 0.7:
        return base_msg + "⚠ MODERATE CONFIDENCE: Plan is useful but may need refinement for your specific situation."
    else:
        return base_msg + "⚠ LOW CONFIDENCE: Plan needs review - try uploading syllabi or providing more details."


@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """Run evaluation harness"""
    try:
        initialize_planner()
        from evaluator import run_evaluation_silent
        results = run_evaluation_silent()
        return jsonify(results), 200
    except Exception as e:
        print(f"✗ Error in evaluate: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Evaluation failed: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    from utils import is_demo_mode
    return jsonify({'status': 'ok', 'demo_mode': is_demo_mode()}), 200


if __name__ == '__main__':
    # Enable demo mode if no API key
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["DEMO_MODE"] = "true"
    
    print("\n✓ Flask web app starting...")
    print("✓ Open your browser to: http://localhost:8000\n")
    app.run(debug=True, port=8000)
