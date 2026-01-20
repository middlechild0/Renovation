"""
Task Registry: Prevent duplicate processing and track workflow state
Creates additive tables in businesses.db without disrupting existing schema.
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

DB_PATH = Path(os.getenv("DB_PATH", "businesses.db"))

SCHEMA_TASK_REGISTRY = """
CREATE TABLE IF NOT EXISTS task_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT UNIQUE NOT NULL,
    workflow_type TEXT NOT NULL,
    business_fsq_id TEXT,
    status TEXT DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    agent_outputs TEXT,
    retry_count INTEGER DEFAULT 0,
    error_log TEXT
);
"""

SCHEMA_WORKFLOW_LOCKS = """
CREATE TABLE IF NOT EXISTS workflow_locks (
    workflow_type TEXT PRIMARY KEY,
    locked_by TEXT,
    locked_at TIMESTAMP,
    expires_at TIMESTAMP
);
"""


class TaskRegistry:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DB_PATH
        self._ensure_tables()

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def _ensure_tables(self) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(SCHEMA_TASK_REGISTRY)
        cur.execute(SCHEMA_WORKFLOW_LOCKS)
        conn.commit()
        conn.close()

    def exists(self, task_id: str) -> bool:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM task_registry WHERE task_id=?", (task_id,))
        row = cur.fetchone()
        conn.close()
        return row is not None

    def mark_started(self, task_id: str, workflow_type: str, business_fsq_id: Optional[str]) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO task_registry (task_id, workflow_type, business_fsq_id, status, started_at) VALUES (?,?,?,?,?)",
            (task_id, workflow_type, business_fsq_id, "in_progress", datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()

    def mark_completed(self, task_id: str, agent_outputs: Dict[str, Any] | None = None) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE task_registry SET status=?, completed_at=?, agent_outputs=? WHERE task_id=?",
            ("completed", datetime.now().isoformat(), json_dumps(agent_outputs), task_id),
        )
        conn.commit()
        conn.close()

    def mark_failed(self, task_id: str, error_log: str) -> None:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE task_registry SET status=?, error_log=? WHERE task_id=?",
            ("failed", error_log, task_id),
        )
        conn.commit()
        conn.close()


def json_dumps(obj: Dict[str, Any] | None) -> str:
    import json
    try:
        return json.dumps(obj or {})
    except Exception:
        return "{}"


__all__ = ["TaskRegistry"]
