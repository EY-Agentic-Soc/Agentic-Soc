# Agentic SOC Raw-Only Dataset v2

This pack contains only raw telemetry and org metadata for a static-data SOC prototype.

Included files:
- users.csv
- assets.csv
- auth_logs.csv
- endpoint_logs.csv
- dns_logs.csv
- proxy_logs.csv
- email_logs.csv
- cloudtrail_logs.csv
- schemas.json

Excluded on purpose:
- alerts / detections
- incidents / case grouping
- threat intel reputation
- analyst feedback
- ground-truth labels
- confidence scores / severity hints / threat flags

Notes:
- users.csv and assets.csv are retained as organization metadata required for investigations.
- All raw events remain timestamped and cross-reference users/hosts consistently.
- Use your own logic/agents to create alerts, scores, clustering, and incident narratives.
