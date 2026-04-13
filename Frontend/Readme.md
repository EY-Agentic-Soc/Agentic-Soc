
# Agentic SOC – Frontend (SOC UI)

## Overview

This repository contains the **Frontend (SOC UI)** for the Agentic SOC system.

The frontend focuses on building a **professional, SOC-style web interface** that enables:
- Alert triage
- Incident investigation
- Agent decision explainability
- Response action simulation
- Learning from resolved incidents

The UI is designed for **clarity, scalability, and real SOC workflows**, not cosmetic visuals.

---

## Tech Stack (Frontend Only)

- **React** – component-based UI
- **Tailwind CSS** – utility-first styling
- **TypeScript** – recommended for type safety and maintainability
- **Mock / API-based data layer** depending on backend readiness

---

## Application Navigation

The frontend UI is organized into the following top-level tabs:

- **Alerts**
- **Incidents**
- **Investigation**
- **Response**
- **Learning**

Each tab represents a major SOC workflow.

---

## Frontend Functional Scope

### Alerts
- Display incoming alerts in a list or table
- Fields:
  - Severity (Critical / High / Medium / Low)
  - Status (Open / Acknowledged / Resolved)
  - Alert summary
  - Source / rule
  - Timestamp
- Alerts are clickable to drill into incident context

---

### Incidents (Dashboard)
- High-level SOC dashboard view
- KPI cards (example):
  - Active incidents
  - Critical incidents
  - Mean Time To Respond (MTTR)
- Severity distribution and recent activity

---

### Investigation
- **Incident Timeline View**
  - Chronological events including:
    - Alert triggers
    - Agent actions
    - Analyst decisions
- **Agent Explanation Panel**
  - Why the agent took an action
  - Evidence used
  - Confidence level
  - Alternative actions considered

This view emphasizes **explainability and trust in agent behavior**.

---

### Response
- **Action Simulation UI**
  - Select response actions (e.g., isolate host, block IP)
  - Display risk indicators and prerequisites
  - Preview simulated outcomes
  - Simulation only (no real execution)

---

### Learning
- View resolved incidents
- Lessons learned
- Agent insights and recommendations
- Search and filter historical incidents

---

## UI & Design Guidelines

- Dark theme (SOC-style)
- Severity-based color indicators
- Consistent spacing (8px system)
- Clear typography hierarchy
- Reusable components (cards, tables, badges, panels)
- Optimized for desktop SOC monitors

Visual polish is secondary to **usability and information hierarchy**.

---

## Recommended Project Structure
```bash
src/
├── components/
│   ├── alerts/
│   ├── incidents/
│   ├── investigation/
│   ├── response/
│   ├── learning/
│   └── common/
├── pages/
│   ├── Alerts.tsx
│   ├── Incidents.tsx
│   ├── Investigation.tsx
│   ├── Response.tsx
│   └── Learning.tsx
├── services/
│   ├── api.ts
│   └── mockData.ts
├── types/
├── layouts/
└── store/


This structure supports modular development and frontend ownership clarity.

```

## Getting Started (Frontend)

### Install dependencies
```bash
npm install 
```

### Start development server
```bash
npm run dev 
```


