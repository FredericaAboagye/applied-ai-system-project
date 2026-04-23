import os
from typing import List

import openai


def require_openai_key(require: bool = True) -> None:
    if require and not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is required. Set it with export OPENAI_API_KEY=your_key."
        )


def is_demo_mode() -> bool:
    return os.getenv("DEMO_MODE", "false").lower() == "true"


def validate_request(request: str) -> str:
    if not request or not request.strip():
        raise ValueError("Prompt cannot be empty.")
    if len(request.strip()) < 15:
        raise ValueError("Please provide a more detailed planning prompt.")
    return request.strip()


def ask_openai_chat(prompt: str) -> str:
    if is_demo_mode():
        return get_demo_response(prompt)
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an academic planner assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.8,
    )
    return completion.choices[0].message.content


def get_demo_response(prompt: str) -> str:
    """Generate a demo response without calling OpenAI API."""
    if "finals" in prompt.lower():
        return """## Finals Week Study Plan

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

**Self-Review:** This plan prioritizes both depth and wellness, grounding recommendations in spaced repetition research."""
    
    elif "semester" in prompt.lower() or "balance" in prompt.lower():
        return """## Semester Balance Plan

**Primary Goals:**
1. Maintain consistent academic progress across all courses
2. Build professional network through job search activities
3. Protect mental health with scheduled breaks and social time

**Weekly Routine (15-20 hrs academic + 5 hrs personal):**
- Monday-Wednesday: Heavy coursework and homework sessions (4 hrs/day), watch for upcoming deadlines
- Thursday: Job search and application work (2 hrs), then social/fun activity
- Friday-Saturday: Study review, catch-up work (2 hrs), then recreation
- Sunday: Planning session to review deadline calendar, rest day, meal prep

**Homework Priorities & Deadlines:**
- Track all assignment deadlines with 1-week buffer
- 60% effort on core major courses with near-term deadline requirements
- 25% effort on electives and general education
- 15% buffer for unexpected assignments or deadline changes

**Job Search Schedule:**
- Tuesday/Thursday evenings: Research and apply (1 hr each)
- Sundays: Update resume and portfolio (1 hr)

**Breaks & Wellness:**
- Daily 30-min movement (walking, gym, yoga)
- One full weekend adventure per month
- Weekly friend time or hobby (2-3 hrs)

**Project & Deadline Management:**
- Create a shared calendar for all major project deadlines
- Set internal deadlines 2 days before submission to allow for review

**Self-Review:** This plan acknowledges realistic time constraints and builds in protection for both academic and personal success."""
    
    else:
        return """## Academic Planning Guide

**Key Sections:**
1. **Goals:** Clear, measurable academic and personal objectives
2. **Weekly Structure:** Consistent routine for work and rest
3. **Homework & Study:** Allocated time blocks with realistic estimates
4. **Breaks & Wellness:** Scheduled recovery to prevent burnout
5. **Job Search (optional):** Dedicated windows for career prep

**Recommendation:** Start by identifying your top 3 priorities this semester, then schedule protected time for each. Use the Pomodoro Technique (25min work, 5min break) to stay focused and maintain energy.

**Self-Review:** This framework balances academic rigor with realistic wellness practices."""

def create_prompt(request: str, sources: List[str]) -> str:
    source_text = "\n\n---\n\n".join(sources) if sources else "No source tips available."
    return (
        "You are a semester planning assistant for a student. Use the retrieved planning tips below to create a detailed, balanced academic plan. "
        "Include explicit sections for goals, weekly structure, homework time, study review, breaks, and job search or wellness actions when relevant. "
        "Do not invent source content; if the requested detail is not supported, label it as a recommendation objective.\n\n"
        f"Student prompt: {request}\n\n"
        "Planning tips:\n"
        f"{source_text}\n\n"
        "Write the plan with numbered sections and a short introduction explaining the main strategy."
    )


def create_review_prompt(request: str, plan_text: str, sources: List[str]) -> str:
    source_text = "\n\n---\n\n".join(sources) if sources else "No source tips available."
    return (
        "You are reviewing a semester plan created for a student. Check the plan for these reliability points:\n"
        "1. Does it clearly reference the student request?\n"
        "2. Does it include at least three plan categories (for example, goals, homework, study, breaks, job search)?\n"
        "3. Does it avoid making unsupported claims that are not reflected in the retrieved tips?\n"
        "4. Does it suggest balanced pacing and wellness breaks?\n\n"
        f"Student prompt: {request}\n\n"
        "Generated plan:\n"
        f"{plan_text}\n\n"
        "Retrieved tips:\n"
        f"{source_text}\n\n"
        "Write a short self-review summary with one sentence for each reliability question and a final confidence statement."
    )


def calculate_confidence(plan_text: str, sources: List[str], review_text: str) -> float:
    """Calculate confidence score (0.0 to 1.0) based on grounding and quality indicators."""
    score = 0.7  # baseline
    
    # Boost if plan is well-structured
    if plan_text.count('\n') > 5:
        score += 0.1
    
    # Boost if sources were retrieved
    if sources and len(sources) >= 2:
        score += 0.1
    
    # Boost if review is positive
    if "clear" in review_text.lower() and "supported" in review_text.lower():
        score += 0.05
    
    # Penalize if suspicious phrases appear
    if "i cannot" in plan_text.lower() or "unable" in plan_text.lower():
        score -= 0.15
    
    return min(1.0, max(0.0, score))
