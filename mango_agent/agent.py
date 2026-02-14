"""MangoAI Agent — Sales Copilot for Mango Reach.

Root agent definition using Google ADK with GPT-4o via LiteLLM.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .prompts import SYSTEM_INSTRUCTION
from .tools.lead_tools import get_leads, get_lead_details
from .tools.email_tools import update_email_placeholders
from .tools.linkedin_tools import update_linkedin_message


root_agent = Agent(
    name="mango_ai",
    model=LiteLlm(model="openai/gpt-4o"),
    description="MangoAI — Agente de Inteligência de Vendas da Magic Mango. "
                "Ajuda a equipe comercial com leads, emails, mensagens LinkedIn e pitches.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        get_leads,
        get_lead_details,
        update_email_placeholders,
        update_linkedin_message,
    ],
)
