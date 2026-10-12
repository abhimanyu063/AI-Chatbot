
from typing import Any


def plan_query(message: str) -> dict[str, Any]:
    """
    Initial rule-based query planner.

    Future implementation:
    - LLM-based intent classification
    - Product and competitor extraction
    - Multi-intent decomposition
    - Ambiguous query handling
    """

    question = message.lower()

    if any(
        keyword in question
        for keyword in ["amazon", "walmart", "costco", "competitor"]
    ):
        intent = "competitor_comparison"
        requires_research = True

    elif any(
        keyword in question
        for keyword in ["sales", "revenue", "declining"]
    ):
        intent = "sales_analysis"
        requires_research = False

    elif any(
        keyword in question
        for keyword in ["profit", "margin", "profitability"]
    ):
        intent = "profit_analysis"
        requires_research = False

    else:
        intent = "general_query"
        requires_research = False

    return {
        "intent": intent,
        "requires_research": requires_research,
        "original_question": message,
    }
