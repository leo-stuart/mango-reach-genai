"""Chat Use Case.

Orchestrates the chat interaction between the user and the agent.
"""

from api.infrastructure.agent.adk_runner import agent_runner
from api.presentation.schemas.chat import ChatRequest, ChatResponse


class ChatUseCase:
    """Use case for chatting with the AI agent."""

    def __init__(self, runner):
        self.runner = runner

    async def execute(self, user_email: str, token: str, request: ChatRequest) -> ChatResponse:
        """Process a chat request."""
        return await self.runner.run_chat(user_email, token, request)


# Singleton instance for dependency injection
chat_use_case = ChatUseCase(agent_runner)
