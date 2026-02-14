"""Lead-related tools for the MangoAI agent.

These tools allow the agent to list leads and fetch full lead details
(research, generated emails, LinkedIn messages) from the Mango Reach API.
"""

from google.adk.tools import ToolContext
from .mango_reach_client import api_get


async def get_leads(skip: int = 0, limit: int = 20, tool_context: ToolContext = None) -> dict:
    """Retrieves a list of leads with summary information.

    Use this tool when the user wants to see their leads, search for a lead,
    or needs an overview of available leads. Returns basic info like name,
    email, company, and whether research/emails/LinkedIn have been generated.

    Args:
        skip: Number of leads to skip (for pagination). Default 0.
        limit: Maximum number of leads to return. Default 20, max 50.

    Returns:
        dict: A dictionary with 'status' and either 'leads' (list) or 'error_message'.
    """
    token = tool_context.state.get("user_token", "") if tool_context else ""
    if not token:
        return {"status": "error", "error_message": "No authentication token available."}

    try:
        leads = await api_get("/leads", token, params={"skip": skip, "limit": min(limit, 50)})
        return {
            "status": "success",
            "total_returned": len(leads),
            "leads": leads,
        }
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to fetch leads: {str(e)}"}


async def get_lead_details(lead_id: int, tool_context: ToolContext = None) -> dict:
    """Retrieves complete details for a specific lead.

    Returns all data including research analysis (company summary, industry,
    pain points, recent news), generated email sequences (with placeholders
    for each day), and LinkedIn message sequences. Use this when the user
    drags a lead into the conversation or asks about a specific lead.

    Args:
        lead_id: The numeric ID of the lead to fetch.

    Returns:
        dict: A dictionary with 'status' and either 'lead' (full details) or 'error_message'.
    """
    token = tool_context.state.get("user_token", "") if tool_context else ""
    if not token:
        return {"status": "error", "error_message": "No authentication token available."}

    try:
        lead = await api_get(f"/leads/{lead_id}", token)
        return {"status": "success", "lead": lead}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to fetch lead {lead_id}: {str(e)}"}
