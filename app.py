import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__, template_folder='templates')

# In-memory store for account database
ACCOUNTS = {
    "autodesk": {
        "id": "autodesk",
        "name": "Autodesk, Inc.",
        "tier": "Premium Enterprise",
        "arr": 1250000,
        "escalations": 242,
        "avg_mttr": "24.2h",
        "sla_status": "Critical",
        "sla_countdown": "01h 45m remaining",
        "churn_risk": "Critical",
        "nrr_risk": 87,
        "active_tickets": 18,
        "sla_limit": "24h",
        "logo_text": "AD",
        "health_score": 38,
        "contract_start": "2024-03-12"
    },
    "vanguard": {
        "id": "vanguard",
        "name": "The Vanguard Group",
        "tier": "Enterprise Platinum",
        "arr": 3400000,
        "escalations": 120,
        "avg_mttr": "8.5h",
        "sla_status": "Warning",
        "sla_countdown": "04h 12m remaining",
        "churn_risk": "Warning",
        "nrr_risk": 64,
        "active_tickets": 8,
        "sla_limit": "12h",
        "logo_text": "VG",
        "health_score": 62,
        "contract_start": "2023-11-01"
    },
    "novartis": {
        "id": "novartis",
        "name": "Novartis AG",
        "tier": "Global Core",
        "arr": 2100000,
        "escalations": 85,
        "avg_mttr": "14.1h",
        "sla_status": "Warning",
        "sla_countdown": "08h 30m remaining",
        "churn_risk": "Warning",
        "nrr_risk": 52,
        "active_tickets": 6,
        "sla_limit": "12h",
        "logo_text": "NV",
        "health_score": 68,
        "contract_start": "2024-01-15"
    },
    "snowflake": {
        "id": "snowflake",
        "name": "Snowflake Inc.",
        "tier": "Strategic Enterprise",
        "arr": 4500000,
        "escalations": 45,
        "avg_mttr": "3.2h",
        "sla_status": "Stabilized",
        "sla_countdown": "SLA Compliant",
        "churn_risk": "Healthy",
        "nrr_risk": 18,
        "active_tickets": 2,
        "sla_limit": "8h",
        "logo_text": "SF",
        "health_score": 94,
        "contract_start": "2022-08-20"
    },
    "constellation": {
        "id": "constellation",
        "name": "Constellation Software",
        "tier": "Premium Enterprise",
        "arr": 1800000,
        "escalations": 190,
        "avg_mttr": "19.8h",
        "sla_status": "Critical",
        "sla_countdown": "02h 15m remaining",
        "churn_risk": "Critical",
        "nrr_risk": 79,
        "active_tickets": 14,
        "sla_limit": "24h",
        "logo_text": "CS",
        "health_score": 45,
        "contract_start": "2024-05-10"
    }
}

DIAGNOSIS = {
    "autodesk": {
        "rca": "A high-severity code regression in version 4.2.1 of the LLM parser microservice caused a 400% query evaluation latency spike in the Autodesk-specific container. As latency rose, Autodesk's automated systems initiated rapid client-side retries, creating an API call loop that saturated regional gateways. Support queue is backing up with 18 open critical tickets.",
        "playbook": [
            {"step": 1, "action": "T1 Autopilot Route", "detail": "Deploy autonomous container rollback to v4.2.0 in the Autodesk isolated cluster.", "status": "Executing"},
            {"step": 2, "action": "Engineering Escalation", "detail": "Raise P0 Incident Flag in Slack channel #ai-core-triage and page Core Platform lead.", "status": "Pending"},
            {"step": 3, "action": "CSM Alerting", "detail": "Send pre-formatted system latency apology and updates to Autodesk Account Director.", "status": "Pending"},
            {"step": 4, "action": "Validation Agent", "detail": "Run synthetic response-time telemetry check. Target response time < 250ms.", "status": "Pending"}
        ]
    },
    "vanguard": {
        "rca": "Security token expiration inside Vanguard's private AWS VPC endpoint has disconnected the Sentinel monitoring agents. Vanguard's backend is rejecting incoming telemetry payloads. Without telemetry streams, Vanguard's SLA risk health score is blind-dropping, triggering warning state. Active ticket volume is steady but monitoring signals are completely down.",
        "playbook": [
            {"step": 1, "action": "Credential Rotation", "detail": "Initiate automated AWS IAM role credential rotation via Vault secret engine.", "status": "Executing"},
            {"step": 2, "action": "Connection Ping", "detail": "Trigger Sentinel VPC Agent heartbeat challenge to private endpoint.", "status": "Pending"},
            {"step": 3, "action": "Client Communication", "detail": "Deliver API connection status report to Vanguard Security Operations Center (SOC).", "status": "Pending"}
        ]
    },
    "novartis": {
        "rca": "Novartis' clinical research translation batch job exceeded their concurrent daily token limit. Requests are hitting standard HTTP 429 (Too Many Requests) errors. Support tickets are piling up from global researchers locked out of the analysis platform. The contract limits have reached maximum density.",
        "playbook": [
            {"step": 1, "action": "Temporary Quota Increase", "detail": "Auto-apply temporary 50B token overlay limit valid for the next 48 hours.", "status": "Executing"},
            {"step": 2, "action": "Researcher Communication", "detail": "Notify research admins that throttle has been lifted and suggest batch offloading hours.", "status": "Pending"},
            {"step": 3, "action": "CRM Lead Sync", "detail": "Create automatic upsell deal in HubSpot for account manager review.", "status": "Pending"}
        ]
    },
    "snowflake": {
        "rca": "Account status is highly stabilized. Low overall ticket volume. The current open tickets relate to minor client-side configuration tweaks. System is performing within standard SLA boundaries. Health metrics are top tier.",
        "playbook": [
            {"step": 1, "action": "Heartbeat Check", "detail": "Maintain normal 60-second status polling.", "status": "Running"},
            {"step": 2, "action": "Autopilot Close", "detail": "Auto-resolve configuration tickets using trained customer success AI responders.", "status": "Completed"}
        ]
    },
    "constellation": {
        "rca": "A critical regional data pipeline outage in East US 2 caused parser failures. The custom parser for Constellation's financial data ingest pipeline is failing with NullPointerExceptions due to undocumented upstream schema shifts in their incoming payload. 14 tickets are currently outstanding.",
        "playbook": [
            {"step": 1, "action": "Schema Alignment", "detail": "Trigger LLM schema mapper to analyze incoming JSON payloads and align keys.", "status": "Executing"},
            {"step": 2, "action": "Data Rerouting", "detail": "Reroute live data streams to backup node in West US 2.", "status": "Pending"},
            {"step": 3, "action": "War Room Setup", "detail": "Initiate developer-triage war room link and notify engineering leads.", "status": "Pending"}
        ]
    }
}

# Global state for Prompt Playground rules
CUSTOM_GUIDELINES = {
    "text": "Prioritize premium accounts with less than 12 hours left on SLA, and auto-escalate core microservice latencies to P0.",
    "last_optimized": "Never",
    "status": "System Default Ruleset"
}


@app.route('/')
def index():
    html = render_template('index.html')
    return html.replace('const startTimestamp = null;', 'let startTimestamp = null;')


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    return jsonify(list(ACCOUNTS.values()))


@app.route('/api/diagnose/<account_id>', methods=['GET'])
def get_diagnose(account_id):
    account_id = account_id.lower()
    if account_id in DIAGNOSIS:
        return jsonify({
            "account": ACCOUNTS[account_id],
            "diagnosis": DIAGNOSIS[account_id]
        })
    return jsonify({"error": "Account not found"}), 404


@app.route('/api/optimize', methods=['POST'])
def optimize_agents():
    data = request.get_json(silent=True) or {}
    guidelines = data.get("guidelines", "").strip()
    if not guidelines:
        return jsonify({"status": "error", "message": "Guidelines cannot be empty"}), 400

    CUSTOM_GUIDELINES["text"] = guidelines
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    CUSTOM_GUIDELINES["last_optimized"] = timestamp
    CUSTOM_GUIDELINES["status"] = "Optimized via Prompt Playground"

    rules_count = len(guidelines.split(","))

    return jsonify({
        "status": "success",
        "message": "Sentinel AI Agent Fleet Re-Optimized Successfully!",
        "details": {
            "timestamp": timestamp,
            "rules_applied_count": rules_count,
            "active_instructions": guidelines[:120] + "..." if len(guidelines) > 120 else guidelines,
            "validation_score": "98.7% Confidence",
            "impact_forecast": "SLA compliance expected to increase by 4.2% over next 48h."
        }
    })


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '').lower() in ('1', 'true', 'yes', 'on')
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
