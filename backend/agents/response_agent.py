from utils.logger import get_logger

logger = get_logger(__name__)

def run_response_agent(incident_state: dict) -> dict:
    logger.info("Response Agent started")

    decision = incident_state.get("decision_output", {})
    entities = incident_state.get("entities", {})
    action = decision.get("recommended_action")

    actions_taken = []

    if action == "disable_account":
        for user in entities.get("users", []):
            actions_taken.append({
                "action": "disable_account",
                "target": user,
                "status": "simulated_success"
            })

    elif action == "isolate_host":
        for host in entities.get("hosts", []):
            actions_taken.append({
                "action": "isolate_host",
                "target": host,
                "status": "simulated_success"
            })

    elif action == "reset_credentials":
        for user in entities.get("users", []):
            actions_taken.append({
                "action": "reset_credentials",
                "target": user,
                "status": "simulated_success"
            })

    elif action == "monitor_only":
        actions_taken.append({
            "action": "monitor_only",
            "target": "incident",
            "status": "logged"
        })

    incident_state["response_output"] = {
        "actions": actions_taken
    }

    logger.info("Response Agent completed")
    return incident_state