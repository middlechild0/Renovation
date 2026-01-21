"""
Feature Flag Manager: percentage rollouts and context targeting
- Loads Renovation/config/feature_flags.json
- is_enabled(feature, context) returns boolean
"""

import os
import json
import random
from pathlib import Path
from typing import Dict, Any

FLAGS_PATH = Path(os.getenv("FEATURE_FLAGS_PATH", Path(__file__).parents[2] / "config" / "feature_flags.json"))


class FeatureFlagManager:
    def __init__(self):
        self._flags = {}
        self._load()

    def _load(self) -> None:
        try:
            with open(FLAGS_PATH) as f:
                data = json.load(f)
            self._flags = data.get("features", {})
        except Exception:
            self._flags = {}

    def is_enabled(self, feature_name: str, context: Dict[str, Any] | None = None) -> bool:
        f = self._flags.get(feature_name)
        if not f:
            return False
        if not f.get("enabled", False):
            return False
        pct = int(f.get("rollout_percentage", 100))
        # Context-based enablement example: tier targeting
        enabled_for = f.get("enabled_for") or []
        if enabled_for and context:
            tier = (context.get("tier") or "").lower()
            if "tier_1_leads" in enabled_for and tier != "tier 1":
                return False
        # Percentage rollout
        return random.randint(1, 100) <= pct

    def enable_for_percentage(self, feature_name: str, percentage: int) -> None:
        f = self._flags.setdefault(feature_name, {})
        f["enabled"] = True
        f["rollout_percentage"] = max(0, min(100, percentage))


__all__ = ["FeatureFlagManager"]
