
from pydantic import BaseModel, Field


class DashboardContext(BaseModel):
    productId: str | None = None
    productName: str | None = None
    category: str | None = None
    dateRange: str | None = None


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    dashboard_context: DashboardContext | None = None


class Citation(BaseModel):
    title: str
    url: str
    source: str | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
