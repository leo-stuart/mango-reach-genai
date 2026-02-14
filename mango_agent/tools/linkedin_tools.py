"""LinkedIn-related tools for the MangoAI agent.

These tools allow the agent to update LinkedIn message content
for generated message sequences on specific leads.
"""

from google.adk.tools import ToolContext
from .mango_reach_client import api_patch


VALID_MESSAGE_TYPES = {
    "connection_request",
    "ice_breaker",
    "soft_pitch_no",
    "soft_pitch_yes",
    "final_followup",
}


async def update_linkedin_message(
    lead_id: int,
    message_type: str,
    content: str,
    tool_context: ToolContext = None,
) -> dict:
    """Updates the content of a LinkedIn message for a specific lead.

    Use this when the user wants to edit or improve a generated LinkedIn message.

    Valid message_type values:
    - "connection_request": Initial connection request message
    - "ice_breaker": First message after connection is accepted
    - "soft_pitch_no": Follow-up if they haven't responded
    - "soft_pitch_yes": Follow-up if they responded positively
    - "final_followup": Final follow-up message

    Args:
        lead_id: The numeric ID of the lead.
        message_type: The type of LinkedIn message to update.
        content: The new content for the LinkedIn message.

    Returns:
        dict: A dictionary with 'status' and either the updated message or 'error_message'.
    """
    token = tool_context.state.get("user_token", "") if tool_context else ""
    if not token:
        return {"status": "error", "error_message": "No authentication token available."}

    if message_type not in VALID_MESSAGE_TYPES:
        return {
            "status": "error",
            "error_message": f"Invalid message_type '{message_type}'. Must be one of: {', '.join(VALID_MESSAGE_TYPES)}",
        }

    try:
        result = await api_patch(
            f"/leads/{lead_id}/linkedin/{message_type}",
            token,
            body={"content": content},
        )
        return {"status": "success", "updated_message": result}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to update LinkedIn message: {str(e)}"}
