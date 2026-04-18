# Enterprise SSO & Access Monitoring Dashboard

A monitoring platform that ingests authentication logs from enterprise SaaS integrations
and detects access failures, provisioning errors, and federation anomalies across a
simulated multi-tenant environment.

## Stack
- Backend: Python, Flask, SQLite
- Frontend: HTML/CSS/JS, Chart.js
- Protocols Monitored: SAML, OIDC, OAuth2

## Setup
1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r backend/requirements.txt
4. cd backend
5. python ingestor.py
6. python alerting.py
7. python app.py
Then open frontend/dashboard.html in your browser.

## API Endpoints
- /api/stats
- /api/logs
- /api/alerts
- /api/by-tenant
- /api/by-protocol
- /api/error-codes
