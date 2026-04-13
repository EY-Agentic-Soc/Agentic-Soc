import json
import os

def run_threat_intel_agent(incident_state, retrieval_layer, llm_client):
    """
    Enrich the suspicious observables using local/contextual intelligence.
    """
    print(f"[*] Running Threat Intel Agent for Incident: {incident_state.get('incident_id', 'Unknown')}")
    
    # --- 1. Read observables from Incident State ---
    entities = incident_state.get("entities", {})
    ips = entities.get("ips", [])
    domains = entities.get("domains", [])
    hashes = entities.get("hashes", [])
    
    # Get user context for role anomaly checks
    user_id = incident_state.get("seed_signal", {}).get("initial_entities", {}).get("user_id")
    user_context = incident_state.get("context", {}).get("user_context", {})
    
    # --- 2. Python Pre-processing (Calculate Local Context) ---
    # The retrieval layer should have methods to check historical logs for prevalence
    domain_prevalence = {}
    for domain in domains:
        domain_prevalence[domain] = retrieval_layer.get_domain_prevalence(domain)
        
    ip_prevalence = {}
    for ip in ips:
        ip_prevalence[ip] = retrieval_layer.get_ip_prevalence(ip)
        
    # Optional: fetch a small set of supporting events if they exist from investigation
    supporting_events = incident_state.get("evidence", {}).get("dns_events", [])[:5]
    
    # --- 3. Build the Gemini Input Packet (Matches Image 4 exactly) ---
    input_packet = {
        "observables": {
            "ips": ips,
            "domains": domains,
            "hashes": hashes
        },
        "org_context": {
            "domain_prevalence": domain_prevalence,
            "ip_prevalence": ip_prevalence,
            "user_role_context": user_context.get("role", "Unknown")
        },
        "supporting_events": supporting_events
    }
    
    # --- 4. Call Gemini ---
    prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'threat_intel_prompt.txt')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'threat_intel_output_schema.json')
    
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
        
    prompt = prompt_template.replace("{input_packet}", json.dumps(input_packet, indent=2))
    
    # Ask Gemini to evaluate using the prompt and enforce the JSON schema
    llm_response = llm_client.generate_structured_content(
        prompt=prompt, 
        schema_file=schema_path
    )
    
    # --- 5. Write back to Incident State ---
    ti_output = json.loads(llm_response)
    incident_state["threat_intel_output"] = ti_output
    
    # Log trace
    if "agent_trace" not in incident_state:
        incident_state["agent_trace"] = []
    incident_state["agent_trace"].append("Threat Intel Agent completed local enrichment.")
    
    return incident_state