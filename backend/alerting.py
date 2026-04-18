from db import query, execute, init_db
from datetime import datetime

def run_alerting():
    init_db()
    now = datetime.utcnow().isoformat()

    # Rule 1: >3 failures from same user in last 30 min
    repeated_failures = query("""
        SELECT user_email, tenant_id, COUNT(*) as cnt
        FROM auth_logs
        WHERE status = 'FAILURE'
          AND timestamp >= datetime('now', '-30 minutes')
        GROUP BY user_email, tenant_id
        HAVING cnt > 3
    """)
    for row in repeated_failures:
        execute("""
            INSERT INTO alerts (created_at, alert_type, severity, user_email, tenant_id, message)
            VALUES (?,?,?,?,?,?)
        """, (now, "REPEATED_AUTH_FAILURE", "HIGH", row["user_email"], row["tenant_id"],
              f"{row['cnt']} failures in 30 min for {row['user_email']}"))

    # Rule 2: Federation errors (SAML/OIDC)
    fed_errors = query("""
        SELECT user_email, tenant_id, error_code, COUNT(*) as cnt
        FROM auth_logs
        WHERE error_code IN ('SAML_ASSERTION_INVALID','OIDC_MISMATCH','FEDERATION_ERROR')
          AND timestamp >= datetime('now', '-60 minutes')
        GROUP BY user_email, tenant_id, error_code
        HAVING cnt > 1
    """)
    for row in fed_errors:
        execute("""
            INSERT INTO alerts (created_at, alert_type, severity, user_email, tenant_id, message)
            VALUES (?,?,?,?,?,?)
        """, (now, "FEDERATION_ANOMALY", "CRITICAL", row["user_email"], row["tenant_id"],
              f"Federation error {row['error_code']} x{row['cnt']} for {row['user_email']}"))

    # Rule 3: Provisioning errors
    prov_errors = query("""
        SELECT tenant_id, COUNT(*) as cnt
        FROM auth_logs
        WHERE event_type IN ('PROVISION','DEPROVISION') AND status = 'ERROR'
          AND timestamp >= datetime('now', '-60 minutes')
        GROUP BY tenant_id
        HAVING cnt > 2
    """)
    for row in prov_errors:
        execute("""
            INSERT INTO alerts (created_at, alert_type, severity, tenant_id, message)
            VALUES (?,?,?,?,?)
        """, (now, "PROVISIONING_ERROR", "MEDIUM", row["tenant_id"],
              f"{row['cnt']} provisioning errors in tenant {row['tenant_id']}"))

    print(f"Alerting complete. {len(repeated_failures)+len(fed_errors)+len(prov_errors)} alert groups processed.")

if __name__ == "__main__":
    run_alerting()
