import json
import os

def run_triage_agent(incident_state, retrieval_layer, llm_client):
    """
    Finds suspicious patterns and decides whether they deserve escalation.
    """
    print(f"[*] Running Triage Agent for Incident: {incident_state.get('incident_id', 'Unknown')}")
    
    # --- 1. Read from Incident State ---
    seed_signal = incident_state.get("seed_signal", {})
    initial_entities = seed_signal.get("initial_entities", {})
    time_window = seed_signal.get("time_window", {})
    
    user_id = initial_entities.get("user_id")
    domains = initial_entities.get("domains", [])
    
    start_time = time_window.get("start")
    end_time = time_window.get("end")
    
    # --- 2. Query Retrieval Layer for small slices ---
    # Fetching only the specific data requested in the Image 2 packet
    auth_events = retrieval_layer.get_auth_events(user_id, start_time, end_time) if user_id else []
    dns_events = retrieval_layer.get_dns_events_by_domain(domains[0], start_time, end_time) if domains else []
    proxy_events = retrieval_layer.get_proxy_events_by_domain(domains[0], start_time, end_time) if domains else []
    
    user_context = retrieval_layer.get_user_context(user_id) if user_id else {}
    asset_context = {} # Can be fetched if host is provided
    
    # --- 3. Build the Gemini Input Packet (Matches Image 2 exactly) ---
    input_packet = {
        "seed_signal": seed_signal,
        "auth_events": auth_events,
        "dns_events": dns_events,
        "proxy_events": proxy_events,
        "user_context": user_context,
        "asset_context": asset_context
    }
    
    # --- 4. Call Gemini ---
    # Load prompt template
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'triage_prompt.txt')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'triage_output_schema.json')
    
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
        
    prompt = prompt_template.replace("{input_packet}", json.dumps(input_packet, indent=2))
    
    # Ask Gemini to evaluate using the prompt and enforce the JSON schema
    llm_response = llm_client.generate_structured_content(
        prompt=prompt, 
        schema_file=schema_path
    )
    
    # --- 5. Write back to Incident State ---
    triage_output = json.loads(llm_response)
    incident_state["triage_output"] = triage_output
    
    # Update status based on triage decision
    if triage_output.get("is_suspicious"):
        incident_state["status"] = "triage_escalated"
    else:
        incident_state["status"] = "closed_as_benign"
        
    # Log trace
    if "agent_trace" not in incident_state:
        incident_state["agent_trace"] = []
    incident_state["agent_trace"].append("Triage Agent completed analysis.")
    
    return incident_state