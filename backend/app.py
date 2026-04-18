from flask import Flask, jsonify
from flask_cors import CORS
from db import query, init_db

app = Flask(__name__)
CORS(app)
init_db()

@app.route("/api/stats")
def stats():
    total   = query("SELECT COUNT(*) as c FROM auth_logs")[0]["c"]
    failures= query("SELECT COUNT(*) as c FROM auth_logs WHERE status='FAILURE'")[0]["c"]
    errors  = query("SELECT COUNT(*) as c FROM auth_logs WHERE status='ERROR'")[0]["c"]
    alerts  = query("SELECT COUNT(*) as c FROM alerts WHERE resolved=0")[0]["c"]
    return jsonify({"total_events": total, "failures": failures, "errors": errors, "open_alerts": alerts})

@app.route("/api/logs")
def logs():
    return jsonify(query("SELECT * FROM auth_logs ORDER BY timestamp DESC LIMIT 100"))

@app.route("/api/alerts")
def alerts():
    return jsonify(query("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 50"))

@app.route("/api/by-tenant")
def by_tenant():
    return jsonify(query("""
        SELECT tenant_id,
               SUM(CASE WHEN status='SUCCESS' THEN 1 ELSE 0 END) as success,
               SUM(CASE WHEN status='FAILURE' THEN 1 ELSE 0 END) as failure,
               SUM(CASE WHEN status='ERROR'   THEN 1 ELSE 0 END) as error
        FROM auth_logs GROUP BY tenant_id
    """))

@app.route("/api/by-protocol")
def by_protocol():
    return jsonify(query("SELECT protocol, status, COUNT(*) as cnt FROM auth_logs GROUP BY protocol, status"))

@app.route("/api/error-codes")
def error_codes():
    return jsonify(query("""
        SELECT error_code, COUNT(*) as cnt FROM auth_logs
        WHERE error_code IS NOT NULL GROUP BY error_code ORDER BY cnt DESC
    """))

if __name__ == "__main__":
    app.run(debug=True, port=5050)
