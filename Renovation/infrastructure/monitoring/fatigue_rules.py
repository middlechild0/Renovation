"""
Fatigue Rules: throttle API usage and batch writes
Creates additive table fatigue_metrics and exposes simple checks.
"""

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", "businesses.db"))

SCHEMA_FATIGUE = """
CREATE TABLE IF NOT EXISTS fatigue_metrics (
    id INTEGER PRIMARY KEY,
    metric_type TEXT,
    current_value INTEGER,
    threshold INTEGER,
    last_reset TIMESTAMP,
    is_throttled BOOLEAN DEFAULT FALSE
);
"""


class FatigueMonitor:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DB_PATH
        self._ensure_tables()

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def _ensure_tables(self) -> None:
        conn = self._conn()
        conn.execute(SCHEMA_FATIGUE)
        conn.commit()
        conn.close()

    def get_threshold(self, api_name: str) -> int:
        # Example thresholds; in production, derive from config
        return 66 if api_name.lower() == "foursquare" else 60

    def get_recent_requests(self, api_name: str, window: int = 60) -> int:
        # Stub: integrate with request logs
        return 0

    def check_api_fatigue(self, api_name: str) -> bool:
        return self.get_recent_requests(api_name) > self.get_threshold(api_name)

    def check_database_fatigue(self) -> bool:
        # Stub: integrate with write queue
        return False


__all__ = ["FatigueMonitor"]
