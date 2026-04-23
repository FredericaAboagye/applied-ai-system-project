import argparse

from planner import SemesterPlanner
from evaluator import run_evaluation
from utils import require_openai_key, is_demo_mode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Semester Success Planner: generate academic plans and run reliability tests"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Natural language planning prompt for the semester planner",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Run the evaluation harness on sample prompts",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run in demo mode without OpenAI API key",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Enable demo mode if requested
    if args.demo:
        import os
        os.environ["DEMO_MODE"] = "true"
    
    # Check for API key only if not in demo mode
    if not is_demo_mode():
        require_openai_key(require=True)

    if args.evaluate:
        run_evaluation()
        return

    if not args.prompt:
        print("Please provide --prompt to generate a plan or --evaluate to run tests.")
        print("Use --demo flag to run without OpenAI API key.")
        return

    planner = SemesterPlanner()
    result = planner.generate_plan(args.prompt)

    print("\n=== Semester Success Planner ===\n")
    print(result["plan_text"])
    print("\n--- Confidence Score ---\n")
    print(f"System confidence: {result['confidence']:.2f} / 1.00")
    print("\n--- Self-review ---\n")
    print(result["review_text"])
    print("\n--- Retrieved sources ---\n")
    for i, source in enumerate(result["sources"], 1):
        print(f"{i}. {source[:100].strip()}...")


if __name__ == "__main__":
    main()
