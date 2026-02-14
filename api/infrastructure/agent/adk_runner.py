"""Agent Runner Infrastructure.

Wraps the ADK runner and session service to provide a clean interface
for the application layer to interact with the agent.
"""

import json
import logging
from typing import AsyncGenerator

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from api.infrastructure.config.settings import settings
from api.presentation.schemas.chat import ChatRequest, ChatResponse
from mango_agent.agent import root_agent

logger = logging.getLogger(__name__)

# Initialize ADK components
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=settings.app_name,
    session_service=session_service,
)


async def _get_or_create_session(user_email: str, session_id: str, token: str):
    """Get an existing session or create a new one with the user's token in state."""
    full_session_id = f"{user_email}_{session_id}"

    # Try to get existing session
    session = await session_service.get_session(
        app_name=settings.app_name,
        user_id=user_email,
        session_id=full_session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=settings.app_name,
            user_id=user_email,
            session_id=full_session_id,
            state={"user_token": token},
        )
    else:
        # Update token in case it was refreshed
        session.state["user_token"] = token

    return session


def _build_user_message(request: ChatRequest) -> str:
    """Build the user message with any drag-and-drop context items."""
    parts = []

    if request.context_items:
        context_parts = []
        for item in request.context_items:
            context_parts.append(f"[CONTEXT: {item.type} ID={item.id}]")
        parts.append(
            "O usuário arrastou os seguintes itens para a conversa: "
            + ", ".join(context_parts)
            + ". Use suas ferramentas para buscar os dados completos desses itens."
        )

    parts.append(request.message)
    return "\n\n".join(parts)


class AgentRunner:
    """Infrastructure wrapper for running the ADK agent."""

    async def run_chat(
        self,
        user_email: str,
        token: str,
        request: ChatRequest
    ) -> ChatResponse:
        """Execute a chat turn with the agent."""
        session = await _get_or_create_session(user_email, request.session_id, token)
        user_message = _build_user_message(request)

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        )

        agent_response_text = ""
        tool_calls_log = []

        async for event in runner.run_async(
            user_id=user_email,
            session_id=session.id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    agent_response_text = "\n".join(
                        part.text for part in event.content.parts if part.text
                    )
            else:
                # Log intermediate tool calls
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.function_call:
                            tool_calls_log.append({
                                "tool": part.function_call.name,
                                "args": dict(part.function_call.args) if part.function_call.args else {},
                            })

        return ChatResponse(
            response=agent_response_text,
            session_id=request.session_id,
            tool_calls=tool_calls_log,
        )

    async def run_chat_stream(
        self,
        user_email: str,
        token: str,
        request: ChatRequest,
    ) -> AsyncGenerator[dict, None]:
        """Execute a chat turn, yielding SSE event dicts as they arrive."""
        session = await _get_or_create_session(user_email, request.session_id, token)
        user_message = _build_user_message(request)

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        )

        try:
            async for event in runner.run_async(
                user_id=user_email,
                session_id=session.id,
                new_message=content,
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        text = "\n".join(
                            part.text for part in event.content.parts if part.text
                        )
                        if text:
                            yield {"event": "response", "data": json.dumps({"text": text})}
                else:
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.function_call:
                                tool_data = {
                                    "tool": part.function_call.name,
                                    "args": dict(part.function_call.args) if part.function_call.args else {},
                                }
                                yield {"event": "tool_call", "data": json.dumps(tool_data)}
                            if part.function_response:
                                result_data = {
                                    "tool": part.function_response.name,
                                    "result": dict(part.function_response.response) if part.function_response.response else {},
                                }
                                yield {"event": "tool_result", "data": json.dumps(result_data)}

            yield {"event": "done", "data": json.dumps({"session_id": request.session_id})}
        except Exception as e:
            logger.exception("Streaming chat error")
            yield {"event": "error", "data": json.dumps({"message": str(e)})}

agent_runner = AgentRunner()
