"""
Kill Switches: trigger-based workflow halt and resume
Creates additive table kill_switches and exposes simple API.
"""

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "businesses.db"))

SCHEMA_KILL_SWITCHES = """
CREATE TABLE IF NOT EXISTS kill_switches (
    id INTEGER PRIMARY KEY,
    switch_name TEXT UNIQUE,
    is_active BOOLEAN DEFAULT FALSE,
    triggered_at TIMESTAMP,
    trigger_reason TEXT,
    auto_resume_at TIMESTAMP
);
"""


class KillSwitches:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DB_PATH
        self._ensure_tables()

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def _ensure_tables(self) -> None:
        conn = self._conn()
        conn.execute(SCHEMA_KILL_SWITCHES)
        conn.commit()
        conn.close()

    def set_active(self, name: str, reason: str, hours: int = 24) -> None:
        conn = self._conn()
        auto_resume = (datetime.now() + timedelta(hours=hours)).isoformat()
        conn.execute(
            "INSERT OR REPLACE INTO kill_switches (id, switch_name, is_active, triggered_at, trigger_reason, auto_resume_at) VALUES (?,?,?,?,?,?)",
            (1, name, True, datetime.now().isoformat(), reason, auto_resume),
        )
        conn.commit()
        conn.close()

    def is_active(self, name: str) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT is_active, auto_resume_at FROM kill_switches WHERE switch_name=?", (name,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return False
        is_active, auto_resume_at = row
        # Auto-resume check
        try:
            if auto_resume_at and datetime.fromisoformat(auto_resume_at) <= datetime.now():
                self.clear(name)
                return False
        except Exception:
            pass
        return bool(is_active)

    def clear(self, name: str) -> None:
        conn = self._conn()
        conn.execute("UPDATE kill_switches SET is_active=FALSE WHERE switch_name=?", (name,))
        conn.commit()
        conn.close()


__all__ = ["KillSwitches"]
