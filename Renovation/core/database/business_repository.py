"""
Business Repository: thin abstraction over SQLite for businesses
- Backward-compatible wrapper to prepare for domain layer migration
"""

import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

DB_PATH = Path(os.getenv("DB_PATH", "businesses.db"))


@dataclass
class Business:
    fsq_id: str
    name: str
    website: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    tier: Optional[str]


class BusinessRepository:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path or DB_PATH

    def _conn(self):
        return sqlite3.connect(str(self.db_path))

    def get_by_fsq_id(self, fsq_id: str) -> Optional[Business]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT fsq_id, name, website, phone, email, tier FROM businesses WHERE fsq_id=?", (fsq_id,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return None
        return Business(*row)

    def list_top_tier(self, tier: str = "Tier 1", limit: int = 50) -> List[Business]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT fsq_id, name, website, phone, email, tier FROM businesses WHERE tier=? LIMIT ?", (tier, limit))
        rows = cur.fetchall()
        conn.close()
        return [Business(*r) for r in rows]


__all__ = ["BusinessRepository", "Business"]
