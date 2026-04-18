import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/auth_logs.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS auth_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_email TEXT NOT NULL,
            tenant_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            protocol TEXT NOT NULL,
            status TEXT NOT NULL,
            error_code TEXT,
            ip_address TEXT,
            app_name TEXT
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            user_email TEXT,
            tenant_id TEXT,
            message TEXT,
            resolved INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

def query(sql, params=()):
    conn = get_conn()
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def execute(sql, params=()):
    conn = get_conn()
    conn.execute(sql, params)
    conn.commit()
    conn.close()
