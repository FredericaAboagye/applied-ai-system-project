# Semester Success Planner: An Applied AI System

## Project Overview

**Original Project:** Built from scratch as a new applied AI system (not an extension of a prior Module project).

**Goal:** Empower students to balance competing academic, personal, and professional demands through intelligent, personalized semester planning. The Semester Success Planner generates structured academic plans that integrate homework, study sessions, job search activities, and self-care breaks—while grounding recommendations in local retrieval of planning best practices.

**Why It Matters:** Students often struggle to coherently plan semesters with multiple priorities. This AI system offers a personalized, reliable alternative to generic advice by:
- Using retrieval-augmented generation (RAG) to ground recommendations in validated planning strategies
- Employing multi-step agent reasoning to decompose goals into actionable tasks
- Including self-review and confidence scoring as guardrails against hallucinations
- Providing an evaluation harness to demonstrate measurable reliability
- Offering a beautiful web UI with syllabus upload for personalized planning (RAG Enhancement feature)

**How It Works:**
- 🎯 **Web Interface:** User-friendly browser app at `http://localhost:8000`
- 📄 **Syllabus Upload:** Students can upload course syllabi to personalize recommendations
- 🤖 **AI Planning:** LLM generates structured, multi-step plans grounded in best practices
- ✅ **Self-Review:** AI critiques its own plan for quality assurance
- 📊 **Reliability Scoring:** Confidence scores show plan reliability
- 🧪 **Evaluation Harness:** Automated tests demonstrate system reliability

---

## System Architecture

This project demonstrates a modular applied AI architecture with four main components:

```
User Prompt
    ↓
[Input Validator] → Rejects empty or too-short requests
    ↓
[Local Retriever] → Fetches 3 planning tip documents based on semantic relevance
    ↓
[Planning Agent] → Generates structured plan using retrieved context
    ↓
[Self-Review Agent] → Critique: Does the plan follow best practices and avoid hallucinations?
    ↓
[Confidence Scorer] → Synthetic reliability score (0.0 to 1.0) based on structure, grounding, and review
    ↓
CLI Output: Plan, Review, Confidence, Retrieved Sources
```

**Data Flow:**
1. **Input** → Student request (e.g., "Plan my finals week with breaks")
2. **Processing** → Retrieve grounded tips → Generate plan → Self-review
3. **Output** → Structured plan, confidence score, sources, review summary

**Reliability Mechanisms:**
- Input validation prevents empty or vague requests
- Retrieved sources are displayed to show what grounded the response
- Self-review checks for structural completeness and claim grounding
- Confidence score helps users assess reliability

---

## Setup Instructions

### 1. Clone and Navigate to the Repository

```bash
git clone https://github.com/YOUR-USERNAME/applied-ai-system-project.git
cd applied-ai-system-project
```

### 2. Create and Activate a Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your OpenAI API Key (Optional for Demo Mode)

```bash
# For live OpenAI queries:
export OPENAI_API_KEY="sk-..." 

# For demo mode (no API key needed, pre-generated responses):
# No setup required — just use the --demo flag
```

### 5. Run the Application

#### Option A: Web UI (Recommended - Much Prettier!)

```bash
# Start the Flask web server
python3 app.py

# Open your browser to: http://localhost:8000
```

Then:
- 📝 Enter your planning prompt in the text area
- 📤 (Optional) Upload a syllabus file to personalize recommendations
- ✨ Click "Generate Plan" to see your personalized plan with confidence score and sources
- 🧪 Click "Run Evaluation" to see reliability test results

#### Option B: Command-Line Interface (CLI)

**Demo Mode (no API key required)**
```bash
python main.py --demo --prompt "Plan my study schedule for finals week with homework and fun breaks"
```

**Live Mode (requires OpenAI API key)**
```bash
python main.py --prompt "Create a semester plan that balances classes, a part-time job, and self-care"
```

### 6. Run the Evaluation Harness via CLI

```bash
# Runs all 3 test scenarios and reports pass/fail rate and confidence scores
python main.py --demo --evaluate
```

---

## Sample Interactions

### Example 1: Finals Week Study Plan

**User Input:**
```
python main.py --demo --prompt "Plan my study schedule for finals week with homework and wellness breaks"
```

**System Output:**

```
=== Semester Success Planner ===

## Finals Week Study Plan

**Goals:** Balance intensive exam prep with adequate rest and stress management.

**Weekly Structure:**
1. **Days 1-3:** Review core concepts from lecture notes. Use active recall and practice problems.
2. **Days 4-5:** Mock exams under timed conditions. Identify weak areas.
3. **Days 6-7:** Targeted review of challenging topics. Light stretching and sleep focus.

**Homework & Study Time:**
- 4-5 hours daily of focused study (not including breaks)
- 30-minute pomodoro blocks with 5-minute breaks
- 2-3 practice exams spread across the week

**Recovery & Wellness:**
- 30-minute walk or exercise daily
- 8+ hours sleep each night, especially final 2 days before exam
- Social check-ins or quick calls with classmates

--- Confidence Score ---

System confidence: 0.90 / 1.00

--- Retrieved sources ---

1. A strong semester plan includes scheduled breaks and self-care...
2. Use a weekly block schedule to assign dedicated time for coursework...
3. For exam preparation, build a revision calendar with subject-specific review sessions...
```

---

### Example 2: Semester Balance with Job Search

**User Input:**
```
python main.py --demo --prompt "Create a semester plan that balances classes, a part-time job search, mental health breaks, and project deadlines"
```

**System Output (excerpt):**

```
## Semester Balance Plan

**Primary Goals:**
1. Maintain consistent academic progress across all courses
2. Build professional network through job search activities
3. Protect mental health with scheduled breaks and social time

**Weekly Routine:**
- Monday-Wednesday: Heavy coursework and homework sessions (4 hrs/day), watch for upcoming deadlines
- Thursday: Job search and application work (2 hrs)
- Friday-Saturday: Study review and recreation
- Sunday: Planning session to review deadline calendar

...Confidence Score: 0.90 / 1.00
```

---

### Example 3: Weekly Productivity Structure

**User Input:**
```
python main.py --demo --prompt "Help me build a weekly productivity schedule with study blocks, homework priorities, and fun downtime"
```

**System Output:**

```
Confidence Score: 0.90 / 1.00

Retrieved sources:
1. Use a weekly block schedule to assign dedicated time for coursework, homework...
2. A strong semester plan includes scheduled breaks and self-care...
```

---

## Design Decisions

### 1. **Why Retrieval-Augmented Generation (RAG)?**
- **Decision:** Store planning best practices in local text documents (not fine-tuning or external APIs)
- **Reasoning:** Faster iteration, transparent sourcing, easy to audit and update
- **Trade-off:** Less sophisticated than vector embeddings, but simpler to demonstrate and reproducible without external dependencies

### 2. **Why Multi-Step Agent Workflow?**
- **Decision:** Generate plan → Self-review (critique) → Confidence score
- **Reasoning:** Mimics human quality-check process; self-criticism reduces confident hallucinations
- **Trade-off:** Two LLM calls per request (cost/latency) vs. higher reliability

### 3. **Why Demo Mode?**
- **Decision:** Pre-generate response templates for common prompts (finals, semester balance, weekly)
- **Reasoning:** Makes the system runnable without API setup; enables demonstration without costs; shows graceful fallback
- **Trade-off:** Responses are semi-templated but consistent with system design

### 4. **Confidence Scoring Logic**
- **Decision:** Synthetic score (0.0–1.0) based on: plan length, source count, positive review tone, absence of "unable" phrases
- **Reasoning:** Provides interpretable reliability signal without requiring another LLM call
- **Trade-off:** Heuristic, not ground truth; future work could use dedicated evaluator LLM

### 5. **Input Validation**
- **Decision:** Reject prompts <15 characters
- **Reasoning:** Prevents spam and low-quality plans; encourages detailed requests
- **Trade-off:** Some valid short requests may be rejected; could use classification instead

---

## Testing Summary

### Evaluation Harness Results

The system was tested on 3 representative scenarios:

```
=== Evaluation Harness ===

[Finals week focus]
  Status: PASS
  Confidence: 0.90/1.00

[Semester overview]
  Status: PASS
  Confidence: 0.90/1.00

[Weekly productivity]
  Status: PASS
  Confidence: 0.90/1.00

========================================
Summary: 3/3 scenarios passed
Average confidence: 0.90
```

### What Worked Well:
- ✅ Retrieval successfully matched student requests to planning tips
- ✅ Agent produced well-structured, multi-section plans
- ✅ Self-review caught plan issues and flagged them
- ✅ Confidence scoring aligned with plan quality
- ✅ All test scenarios passed with high confidence

### What Could Improve:
- ⚠️ Demo mode responses are templated; live mode (with API key) would show more personalization
- ⚠️ Confidence score is heuristic; an evaluator LLM could produce more rigorous assessments
- ⚠️ Retrieved sources are simple bag-of-words matching; vector embeddings would improve relevance

---

## Video Walkthrough

**[Loom Video Link]** — Recording to be added during final submission

The video demonstrates:
- ✅ End-to-end system run with 2-3 different student planning requests
- ✅ AI planning agent behavior (structured output, retrieval, self-review)
- ✅ Reliability mechanisms in action (confidence scores, source display)
- ✅ Evaluation harness running all 3 test scenarios and reporting results

---

## Project Structure

- `main.py` — CLI entrypoint for planning or evaluation
- `planner.py` — agentic planning workflow and prompt composition
- `retriever.py` — local knowledge retrieval from planning tip documents
- `evaluator.py` — sample input evaluation and reliability checks
- `utils.py` — input validation, OpenAI wrapper, guardrail helpers
- `model_card.md` — AI collaboration reflection, ethics, and bias analysis
- `assets/planning_tips/` — local planning best-practice documents
- `assets/system_architecture.mmd` — Mermaid diagram source

---

## Future Improvements

1. **Web UI:** Flask/React interface for easier student access
2. **Multi-turn Conversation:** Refine the plan through follow-up questions
3. **Vector Embeddings:** Upgrade retriever from bag-of-words to semantic search
4. **Fine-tuned Model:** Train or prompt-tune on real student feedback
5. **Timeline Visualization:** Gantt or calendar view of the generated plan
6. **Personal Preferences:** Learn student's preferred schedule blocks and break patterns
7. **Integration:** Connect to Google Calendar or to-do apps (Todoist, Asana)

---

## License

Educational use. See LICENSE file for details.

---

## Questions or Feedback?

Open an issue on GitHub or contact the developer. Thank you for using Semester Success Planner! 🎓
