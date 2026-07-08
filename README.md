# Sentinel AI – Enterprise NRR & SLA Risk Dashboard

**Sentinel AI** is a production-ready, high-fidelity operational command center for AI Customer Success Leaders. It is designed to ingest real-time customer success telemetry streams, evaluate major global enterprise accounts for SLA violations, compute live Net Revenue Retention (NRR) risk scores, and dispatch multi-agent triage playbooks.

![Sentinel AI Dashboard Preview](https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80)

---

## Key Core Capabilities

### ⚡ 1. Real-Time Telemetry & Executive Metrics
- **ARR Protection Tracker**: Live monitoring of protected Annual Recurring Revenue ($13.05M portfolio scale).
- **MTTR Optimization**: Real-time tracking of Mean Time to Resolution, highlighting deviations from standard baselines.
- **SLA Countdown Monitors**: Prominent visual alerts for high-risk SLA count-downs (e.g., Autodesk at `<02h` remaining) and green states for stabilized accounts.

### 🔍 2. Proactive Churn Diagnostics (Deep Diagnosis Panel)
- **Root-Cause Analysis (RCA)**: Simulated LLM investigation reports identifying the exact breakdown layer (microservice regressions, API call loops, rate-limits, database schema mismatches).
- **Suggested Agentic Triage Play**: Step-by-step automated workflow displaying sequential actions (autopilot rollbacks, engineering escalations, CSM updates) along with execution status indicators.

### 🎛️ 3. Agentic Prompt Steering (Prompt Playground)
- **Operational Guidelines Form**: Customer Success Directors can input custom natural language rules (e.g., *"Prioritize premium accounts with less than 12 hours left on SLA"*).
- **Simulated Validation Node**: Clicking **Optimize Agents** evaluates guidelines and updates agent model configurations, returning high-confidence impact projections.

---

## Architecture & Tech Stack

- **Backend Engine**: Python with Flask framework.
- **Frontend Layer**: Single-Page UI powered by **Tailwind CSS** (via CDN) with a custom **"Cyberpunk Corporate"** dark-mode design system. 
- **Design Tokens**: Glassmorphic panels, glowing neon cyan/magenta/green outlines, Orbitron telemetry typography, and micro-animations.

---

## Getting Started

### Prerequisites

You need the `uv` Python package manager to provision the correct Python version and dependencies automatically. If not installed, set it up via:

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Local Development Server

To launch the Sentinel AI Dashboard:

1. Clone this repository:
   ```bash
   git clone https://github.com/titashdev-ops/sentinel-ai-dashboard.git
   cd sentinel-ai-dashboard
   ```

2. Spin up the Flask server:
   ```powershell
   $env:PATH = "C:\Users\titas\.local\bin;" + $env:PATH; uv run --with flask python app.py
   ```

3. Open your browser and navigate to:
   **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

*Proprietary Command Center of Sentinel AI Inc. - Confirmed Operational.*
