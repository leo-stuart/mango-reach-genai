"""Email-related tools for the MangoAI agent.

These tools allow the agent to update email placeholders for
generated email sequences on specific leads.
"""

from google.adk.tools import ToolContext
from .mango_reach_client import api_patch, api_post


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


async def send_manual_email(
    recipients: list[str],
    subject: str,
    saudacao: str,
    body: str,
    assinatura: str,
    scheduled_at: str = None,
    tool_context: ToolContext = None,
) -> dict:
    """Sends a manual email to specific recipients, with optional scheduling.

    Use this when the user wants to compose and send an email manually
    (not part of the automated lead email sequence). Always confirm the
    recipient, subject, and content with the user before calling this tool.

    Args:
        recipients: List of email addresses to send to.
        subject: The email subject line.
        saudacao: The greeting/salutation (e.g. "Olá João").
        body: The email body text.
        assinatura: The email signature.
        scheduled_at: Optional ISO datetime string to schedule the email
                      for a future date/time instead of sending immediately.

    Returns:
        dict: A dictionary with 'status' and either the send result
              (batch_id, sent/failed/scheduled counts) or 'error_message'.
    """
    token = tool_context.state.get("user_token", "") if tool_context else ""
    if not token:
        return {"status": "error", "error_message": "No authentication token available."}

    payload = {
        "recipients": recipients,
        "subject": subject,
        "saudacao": saudacao,
        "body": body,
        "assinatura": assinatura,
    }
    if scheduled_at:
        payload["scheduled_at"] = scheduled_at

    try:
        result = await api_post("/manual-email/send", token, body=payload)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to send email: {str(e)}"}
