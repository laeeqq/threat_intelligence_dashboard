
# 🛡️ Threat Intelligence Dashboard

A real-time threat intelligence dashboard that fetches live malicious IPs from AbuseIPDB, stores them in a database, and visualizes them in a custom web dashboard and Grafana.

---

## Tech Stack
- Python, Flask, Pandas, SQLite
- HTML, CSS, JavaScript, Chart.js
- Grafana
- AbuseIPDB API

---

## Features
- Fetches 100 live malicious IPs in real time
- Saves threat data to a local SQLite database
- Custom dark themed web dashboard with charts and tables
- Grafana dashboard for professional SOC visualization
- REST API endpoints for threat data and statistics

---

## How to Run

1. Enter the environment
```bash
nix-shell
```

2. Add your API key to `.env`
```
ABUSEIPDB_KEY=your_key_here
```

3. Run the app
```bash
python3 app.py
```

4. Visit `http://127.0.0.1:5000`

---

## API Endpoints
- `GET /` — Web dashboard
- `GET /api/threats` — Live malicious IPs
- `GET /api/stats` — Threat statistics

---

## Author
Laeeq — Cybersecurity student building real SOC tools from scratch
EOF