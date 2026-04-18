from faker import Faker
from db import init_db, execute
from datetime import datetime, timedelta
import random

fake = Faker()

TENANTS = ["acme-corp", "globex-inc", "initech", "umbrella-co", "cyberdyne"]
APPS    = ["Okta", "Salesforce", "Slack", "Workday", "GitHub", "Zoom"]
PROTOCOLS = ["SAML", "OIDC", "OAuth2"]
EVENT_TYPES = ["LOGIN", "LOGOUT", "TOKEN_REFRESH", "PROVISION", "DEPROVISION"]
STATUSES = ["SUCCESS", "FAILURE", "ERROR"]
ERRORS = [None, "SAML_ASSERTION_INVALID", "TOKEN_EXPIRED", "USER_NOT_FOUND",
          "MFA_TIMEOUT", "OIDC_MISMATCH", "FEDERATION_ERROR", "ACCOUNT_LOCKED"]

def simulate_logs(n=200):
    init_db()
    now = datetime.utcnow()
    for _ in range(n):
        ts = now - timedelta(minutes=random.randint(0, 30))
        status = random.choices(STATUSES, weights=[70, 20, 10])[0]
        error = random.choice(ERRORS) if status != "SUCCESS" else None
        execute("""
            INSERT INTO auth_logs
            (timestamp, user_email, tenant_id, event_type, protocol, status, error_code, ip_address, app_name)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            ts.isoformat(), fake.company_email(), random.choice(TENANTS),
            random.choice(EVENT_TYPES), random.choice(PROTOCOLS),
            status, error, fake.ipv4(), random.choice(APPS)
        ))
    print(f"Inserted {n} simulated auth log entries.")

if __name__ == "__main__":
    simulate_logs()
