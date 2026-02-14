"""Chat routes for the MangoAI agent."""

import logging
from fastapi import APIRouter, Depends

from api.infrastructure.security.jwt_auth import get_current_user_email, get_raw_token
from api.presentation.schemas.chat import ChatRequest, ChatResponse
from api.application.use_cases.chat_with_agent import chat_use_case, ChatUseCase

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/agent/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_email: str = Depends(get_current_user_email),
    token: str = Depends(get_raw_token),
):
    """Send a message to the MangoAI agent and get a response."""
    return await chat_use_case.execute(user_email, token, request)


@router.get("/agent/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "agent": "mango_ai", "model": "gpt-4o"}
