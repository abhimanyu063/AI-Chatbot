
from fastapi import APIRouter

from src.graph import graph
from src.schemas.models import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/api/v1/assistant",
    tags=["AI Assistant"],
)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    React -> FastAPI -> LangGraph -> React
    """

    initial_state = {
    "session_id": request.session_id,
    "question": request.message,
    "dashboard_context": (
        request.dashboard_context.model_dump()
        if request.dashboard_context
        else None
    ),
    }

    result = await graph.ainvoke(initial_state)

    return ChatResponse(
        answer=result["answer"],
        citations=[],
    )
