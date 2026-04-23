from typing import List

from retriever import LocalRetriever
from utils import (
    ask_openai_chat,
    create_prompt,
    create_review_prompt,
    validate_request,
    calculate_confidence,
)


class SemesterPlanner:
    def __init__(self) -> None:
        self.retriever = LocalRetriever("assets/planning_tips")

    def generate_plan(self, request: str) -> dict:
        validated_request = validate_request(request)
        sources = self.retriever.retrieve(validated_request, top_k=3)
        prompt = create_prompt(validated_request, sources)
        plan_text = ask_openai_chat(prompt)

        review_prompt = create_review_prompt(validated_request, plan_text, sources)
        review_text = ask_openai_chat(review_prompt)

        # Calculate confidence score based on grounding and quality
        confidence = calculate_confidence(plan_text, sources, review_text)

        return {
            "plan_text": plan_text.strip(),
            "review_text": review_text.strip(),
            "sources": sources,
            "confidence": confidence,
        }
