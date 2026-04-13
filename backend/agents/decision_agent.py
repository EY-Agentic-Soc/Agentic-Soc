from utils.gemini_client import call_gemini
from utils.logger import get_logger

logger = get_logger(__name__)

def run_decision_agent(incident_state: dict) -> dict:
    logger.info("Decision Agent started")

    investigation = incident_state.get("investigation_output", {})
    threat_intel = incident_state.get("threat_intel_output", {})
    context = incident_state.get("context", {})
    entities = incident_state.get("entities", {})
    timeline = incident_state.get("timeline", [])

    prompt = f"""
You are a SOC Decision Agent.

Your task is to:
- Determine incident severity
- Determine business risk
- Recommend EXACTLY ONE response action

INCIDENT INVESTIGATION:
{investigation}

THREAT INTELLIGENCE:
{threat_intel}

USER / ASSET CONTEXT:
{context}

AFFECTED ENTITIES:
{entities}

TIMELINE:
{timeline}

RULES:
- Do not invent data
- Use only provided information
- Output ONLY valid JSON
- Allowed actions:
  - disable_account
  - isolate_host
  - reset_credentials
  - monitor_only

OUTPUT FORMAT:
{{
  "severity": "low|medium|high",
  "business_risk": "low|medium|high",
  "recommended_action": "<one_action>",
  "confidence": 0.0,
  "justification": "<short explanation>"
}}
"""

    response = call_gemini(prompt)
    decision_output = eval(response)

    incident_state["decision_output"] = decision_output
    logger.info("Decision Agent completed")
    return incident_state

