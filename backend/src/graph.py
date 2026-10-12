
from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from src.agents.planner import plan_query
from src.agents.sql_client import (
    SQLPlannerError,
    sql_planner_client,
)


class AgentState(TypedDict, total=False):
    session_id: str
    question: str
    dashboard_context: dict[str, Any] | None

    intent: str
    requires_research: bool

    sql_result: dict[str, Any]
    sql_error: str | None

    answer: str


def planner_node(state: AgentState) -> dict[str, Any]:
    plan = plan_query(state["question"])

    return {
        "intent": plan["intent"],
        "requires_research": plan["requires_research"],
    }


async def sql_node(state: AgentState) -> dict[str, Any]:
    """
    Fetch internal business metrics through SQL Planner.
    """

    try:
        result = await sql_planner_client.execute(
            question=state["question"],
            session_id=state["session_id"],
            dashboard_context=state.get("dashboard_context"),
        )

        return {
            "sql_result": result,
            "sql_error": None,
        }

    except SQLPlannerError:
        return {
            "sql_result": {},
            "sql_error": "Internal data is currently unavailable.",
        }


def response_node(state: AgentState) -> dict[str, Any]:
    """
    Temporary deterministic response.

    Later replaced with evidence-backed analysis,
    RCA, and recommendations.
    """

    if state.get("sql_error"):
        return {
            "answer": (
                "I couldn't retrieve the internal business "
                "metrics required for this analysis. "
                "Please try again later."
            )
        }

    sql_result = state.get("sql_result", {})

    metrics = sql_result.get("metrics", {})

    if not sql_result.get("data_available", False):
        return {
            "answer": (
                "Internal data is not available for this request. "
                "The Coverage Gate and Research Agent "
                "will be implemented in the next phase."
            )
        }

    source_label = (
        "SIMULATED DATA - NOT REAL TARGET METRICS"
        if sql_result.get("is_mock")
        else "INTERNAL SQL PLANNER DATA"
    )

    metric_lines = "\n".join(
        f"- {key}: {value}"
        for key, value in metrics.items()
    )

    answer = (
        f"[{source_label}]\n\n"
        f"Detected intent: {state.get('intent')}\n"
        f"Product: {sql_result.get('product_name')}\n\n"
        f"Internal metrics:\n{metric_lines}\n\n"
        "This is a SQL Planner integration test, "
        "not a completed root-cause analysis. "
        "Competitor research and recommendations "
        "are not yet implemented."
    )

    return {"answer": answer}


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("sql_planner", sql_node)
    workflow.add_node("response", response_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "sql_planner")
    workflow.add_edge("sql_planner", "response")
    workflow.add_edge("response", END)

    return workflow.compile()


graph = build_graph()
