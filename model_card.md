# Model Card: Semester Success Planner

## 1. AI Collaboration Reflection

### Helpful AI Suggestions During Development

**1. Architectural Design: Plan → Self-Review → Confidence Score Workflow**

The AI suggested the multi-step workflow where the planning agent generates a plan, then a self-review agent critiques it before outputting to the user. This proved highly effective because:
- It mimics how humans review their own work before sharing
- The self-review step explicitly checks for hallucinations and grounding
- Confidence scores give users transparency about reliability
- It naturally demonstrates the "agentic" behavior required by the rubric

**Example Impact:**
- Without self-review, the system might produce an unsupported plan that sounds good but contradicts the retrieval sources
- With self-review, the system flags plans that lack balanced breaks or don't reference the retrieved tips

---

**2. Structured Prompting for Better Plan Organization**

The AI recommended that the planning prompt explicitly ask for sections: "Include explicit sections for goals, weekly structure, homework time, study review, breaks, and job search..."

This was highly effective because:
- Responses became consistently structured across different test cases
- Plans were easier for users to scan and understand
- Evaluation metrics became clearer (we could check for each section)
- It demonstrated that "specialized behavior" (structured prompting) is a legitimate AI feature

---

**3. Demo Mode as a Fallback Strategy**

When I hit API key issues during testing, the AI suggested building a demo mode with pre-generated responses. This proved valuable because:
- Allowed full system testing without external API costs
- Made the project reproducible for anyone (no API key needed)
- Showed graceful degradation patterns (system works in demo if API is down)
- Made the walkthrough video test-friendly

---

### Flawed AI Suggestions During Development

**1. Confidence Scoring Using Embeddings and Semantic Similarity**

The AI initially suggested a sophisticated confidence score based on BERTScore or semantic embeddings—comparing the plan to the retrieval sources to measure alignment.

**Why It Was Flawed:**
- Over-engineered for a teaching project; added complexity and extra dependencies
- Unclear how to debug if scores were wrong (black-box scoring)
- Not necessary to demonstrate "reliability" in the project
- The heuristic approach I implemented instead (checking for required keywords, plan length, review tone) was easier to explain and audit

**Lesson Learned:** Simplicity and transparency matter more than sophistication, especially for educational AI projects.

---

**2. Test Evaluation Metric Using ROUGE/BERTScore**

The AI suggested comparing generated plans to "gold standard" plans using ROUGE (Recall-Oriented Understudy for Gisting Evaluation) or BERTScore from HuggingFace.

**Why It Was Flawed:**
- Added a heavy dependency (transformers library) for a simple classification task
- Plans are inherently diverse; two good plans may differ significantly
- Simple keyword matching ("Does output contain 'finals', 'break', 'homework'?") was sufficient and more interpretable
- The heuristic metric I implemented instead made it easy to add more test cases

**Lesson Learned:** The best evaluation method is often the simplest one that answers your question clearly.

---

**3. Integration with External Planning APIs**

The AI suggested integrating with Google Calendar API or Asana API to convert the plan into live calendar events.

**Why It Was Flawed (for this project):**
- Added scope creep and external dependencies
- Complicated the setup instructions significantly
- The rubric emphasizes reliable AI design, not cool integrations
- The core problem (generating a good plan) wasn't solved yet

**Lesson Learned:** Focus on what the rubric actually requires, not on building a "cool" full-stack product.

---

## 2. System Limitations and Biases

### Limitations

**1. Demographic Assumptions**
- **Assumption:** Students have flexible schedules with dedicated study blocks
- **Reality:** Night-shift workers, students with disabilities, parents, and international students have different constraints
- **Impact:** Generated plans may not fit everyone's life
- **Mitigation:** Could add "constraint input" (e.g., "I work nights" or "I have Friday prayers")

---

**2. Cultural and Wellness Bias**
- **Assumption:** Standard wellness = 8 hours sleep, gym time, social breaks
- **Reality:** Different cultures, neurodivergent people, and introverts may have different wellness needs
- **Impact:** Plans may feel prescriptive rather than empowering
- **Mitigation:** Allow users to customize "wellness activities" instead of suggesting specific ones

---

**3. Academic Domain Bias**
- **Assumption:** Semester = 15-week academic calendar with exams at the end
- **Reality:** Some students are on quarter systems, do accelerated programs, or attend boot camps
- **Impact:** Plans generated for non-standard academic calendars may be misaligned
- **Mitigation:** Add a "semester type" input (semester vs. quarter vs. accelerated)

---

**4. Socioeconomic Assumptions**
- **Assumption:** Job search is a priority alongside academics
- **Reality:** Some students need to prioritize survival (food, housing, childcare) over job searching
- **Impact:** Plan may be tone-deaf to students with limited resources
- **Mitigation:** Make job search optional; add "I need to work X hours/week to pay rent"

---

### Potential Misuses and Safeguards

**Potential Misuse 1: Academic Dishonesty**
- Someone could use the planner to generate fake justifications for late work ("I followed a plan and still couldn't finish")
- **Safeguard:** The system includes sources and confidence scores, not blank guarantees. Teachers can ask to see the actual plan and evaluate its reasonableness.

---

**Potential Misuse 2: Over-reliance Without Critical Thought**
- A student might follow the AI plan blindly without adapting it to their actual needs
- **Safeguard:** The system encourages "you should customize this based on your energy and preferences" in the self-review
- **Better Safeguard:** Add a disclaimer in the CLI output: "This plan is a suggestion. Your actual circumstances may require adjustments."

---

**Potential Misuse 3: Exposing Personal Info**
- If deployed online, students might share sensitive data (medical conditions, family crises) in planning prompts
- **Safeguard:** Current system doesn't store prompts (stateless, demo mode)
- **Better Safeguard:** Add privacy policy if deployed; never log full prompts

---

## 3. What Surprised Me During Testing

**Surprise 1: Self-Review Was More Useful Than Expected**

I initially included self-review just as a "nice-to-have" reliability feature. In practice:
- The self-review often flagged oversights in my own demo responses (missing wellness mentions, no job search integration)
- Users reported trusting the output more when they saw a self-review summary
- It acted as a real sanity check, reducing confident hallucinations

**Takeaway:** Multi-step reasoning isn't just a novelty—it meaningfully improves output quality.

---

**Surprise 2: Confidence Scores Were Harder to Calibrate Than Expected**

I assumed a simple heuristic (plan length + source count + review tone) would work. In practice:
- A short, focused plan scored lower confidence than a long, rambling one, even if the short plan was better
- Adding source count made the system favor over-linking to sources
- Fine-tuning the formula to be fair across different request types was non-trivial

**Takeaway:** Even "simple" reliability metrics need careful thought. Every parameter you add can introduce new biases.

---

**Surprise 3: Demo Mode Responses Were Almost As Good As Live Mode**

I expected demo mode to be a weak fallback. In practice:
- Pre-generated but semantically structured responses (following the same section format) helped users understand the system
- Users couldn't easily tell the difference between demo and live, which suggests the prompt design matters more than raw LLM capability
- Demo mode made the system reproducible and cost-effective

**Takeaway:** Good prompt design and structured outputs matter as much as the underlying model.

---

## 4. Key Takeaways About Responsible AI Design

1. **Transparency > Perfection:** Showing sources and confidence scores (and being honest about heuristics) builds trust better than hiding complexity
2. **Simplicity > Sophistication:** Heuristic reliability metrics are often better than complex ML-based ones for interpretability
3. **Test Early and Often:** The evaluation harness caught issues that I wouldn't have noticed in manual testing
4. **Acknowledge Limitations:** The model card exists because limitations are inevitable—good design means being transparent about them
5. **Bias Is Baked In:** I made assumptions about "good planning" that don't apply to everyone. Future versions need user input on what wellness and success mean

---

## 5. Testing Results Summary

| Scenario | Status | Confidence | Issues |
|----------|--------|-----------|--------|
| Finals week | PASS | 0.90 | None |
| Semester balance | PASS | 0.90 | None |
| Weekly productivity | PASS | 0.90 | None |

**Average Confidence:** 0.90 / 1.00
**Pass Rate:** 100% (3/3)

**Reliability Observations:**
- ✅ All plans included required sections (goals, homework, breaks)
- ✅ Confidence scores were stable across test cases
- ✅ Self-review flagged incomplete plans
- ✅ Retrieved sources were relevant to each request
- ⚠️ Edge cases (very short requests) are not tested; unknown behavior

---

## 6. Recommendations for Future Development

1. **Collect User Feedback:** Deploy with real students and measure: (a) Do they follow the plans? (b) Do plans improve their semester? (c) What adjustments did they make?

2. **Expand Diversity of Training Examples:** Add planning tips for: (a) neurodivergent learners, (b) working students, (c) parents, (d) different cultural contexts

3. **Implement Multi-Turn Conversation:** Allow students to ask follow-up questions and refine their plan iteratively, not just get a one-shot response

4. **Add Personalization:** Remember student preferences (do they prefer morning or afternoon study blocks?) and incorporate into future plans

5. **Benchmark Against Human Planners:** Compare AI-generated plans to plans created by academic advisors; measure student satisfaction

6. **Open-Source Retrieval Documents:** Let students and teachers contribute new planning tips, making the system more community-driven

---

## Conclusion

The Semester Success Planner demonstrates that thoughtful AI system design requires balancing capability (generating good plans), reliability (checking the plans), transparency (showing sources and scores), and fairness (acknowledging who the system works for and where it falls short).

The most important discovery: **AI is only trustworthy when it's honest about its limitations.**
