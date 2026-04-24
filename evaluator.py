
from planner import SemesterPlanner
import os
from typing import Dict, List, Any


SCENARIOS = [
    {
        "name": "Finals week focus",
        "prompt": "I need a plan for finals week with homework, study sessions, and recovery breaks.",
        "required_terms": ["finals", "break", "homework", "review"],
    },
    {
        "name": "Semester overview",
        "prompt": "Create a semester plan that balances classes, a part-time job search, mental health breaks, and project deadlines.",
        "required_terms": ["semester", "job", "break", "deadline"],
    },
    {
        "name": "Weekly productivity",
        "prompt": "Help me build a weekly productivity schedule with study blocks, homework priorities, and fun downtime.",
        "required_terms": ["weekly", "study", "homework"],
    },
]


def run_evaluation() -> None:
    """Run evaluation and print results to console"""
    # Auto-enable demo mode for evaluation if no API key
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["DEMO_MODE"] = "true"
    
    planner = SemesterPlanner()

    print("\n=== Evaluation Harness ===\n")
    passed = 0

    for scenario in SCENARIOS:
        print(f"\n[{scenario['name']}]")
        result = planner.generate_plan(scenario["prompt"])
        plan_text = result["plan_text"].lower()

        missing = [term for term in scenario["required_terms"] if term not in plan_text]
        if missing:
            print(f"  Status: FAIL (missing: {', '.join(missing)})")
        else:
            print("  Status: PASS")
            passed += 1

        print(f"  Confidence: {result['confidence']:.2f}/1.00")
        print(f"  Review preview: {result['review_text'].splitlines()[0][:80]}...")

    print(f"\n{'='*40}")
    print(f"Summary: {passed}/{len(SCENARIOS)} scenarios passed")


def run_evaluation_silent() -> Dict[str, Any]:
    """Run evaluation and return JSON-structured results for API"""
    # Auto-enable demo mode for evaluation if no API key
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["DEMO_MODE"] = "true"
    
    planner = SemesterPlanner()
    results = []
    passed = 0
    total_confidence = 0.0

    for scenario in SCENARIOS:
        result = planner.generate_plan(scenario["prompt"])
        plan_text = result["plan_text"].lower()

        missing = [term for term in scenario["required_terms"] if term not in plan_text]
        scenario_passed = len(missing) == 0
        
        if scenario_passed:
            passed += 1
        
        total_confidence += result['confidence']
        
        results.append({
            "name": scenario['name'],
            "passed": scenario_passed,
            "confidence": result['confidence'],
            "missing_terms": missing
        })

    avg_confidence = total_confidence / len(SCENARIOS) if SCENARIOS else 0.0
    
    return {
        "scenarios": results,
        "passed": passed,
        "total": len(SCENARIOS),
        "avg_confidence": avg_confidence
    }

