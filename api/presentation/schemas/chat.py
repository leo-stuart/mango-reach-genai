"""Pydantic schemas for the MangoAI API."""

from pydantic import BaseModel


class ContextItem(BaseModel):
    """An item dragged into the conversation (lead, email, etc)."""
    type: str  # "lead", "email", "linkedin"
    id: int    # The ID of the item


class ChatRequest(BaseModel):
    """Request body for the /agent/chat endpoint."""
    message: str
    session_id: str = "default"
    context_items: list[ContextItem] = []


class ChatResponse(BaseModel):
    """Response from the /agent/chat endpoint."""
    response: str
    session_id: str
    tool_calls: list[dict] = []
