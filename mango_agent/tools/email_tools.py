"""Email-related tools for the MangoAI agent.

These tools allow the agent to update email placeholders for
generated email sequences on specific leads.
"""

from google.adk.tools import ToolContext
from .mango_reach_client import api_patch


async def update_email_placeholders(
    lead_id: int,
    day: int,
    placeholders: dict,
    tool_context: ToolContext = None,
) -> dict:
    """Updates the placeholders of a generated email for a specific lead and day.

    Use this when the user wants to edit or improve a generated email.
    The placeholders dict should contain the email template variables like
    'subject', 'greeting', 'body_paragraph_1', etc.

    Valid days are: 1, 3, 5, 7 (the email sequence schedule).

    Args:
        lead_id: The numeric ID of the lead.
        day: The day number of the email in the sequence (1, 3, 5, or 7).
        placeholders: Dictionary of email placeholders to update.

    Returns:
        dict: A dictionary with 'status' and either the updated email or 'error_message'.
    """
    token = tool_context.state.get("user_token", "") if tool_context else ""
    if not token:
        return {"status": "error", "error_message": "No authentication token available."}

    try:
        result = await api_patch(
            f"/leads/{lead_id}/emails/{day}",
            token,
            body={"placeholders": placeholders},
        )
        return {"status": "success", "updated_email": result}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to update email: {str(e)}"}
