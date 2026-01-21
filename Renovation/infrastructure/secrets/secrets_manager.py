"""
Secrets Manager: schema-validated secret loading with env fallback
- Validates secrets.json against Renovation/config/secrets.schema.json
- Provides type-safe getters and rotation stubs
"""

import os
import json
from pathlib import Path
from typing import Any, Optional

try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
except Exception:
    validate = None
    ValidationError = Exception

SCHEMA_PATH = Path(__file__).parents[2] / "config" / "secrets.schema.json"
DEFAULT_SECRETS_PATH = Path(os.getenv("SECRETS_PATH", "secrets.json"))


class SecretsManager:
    def __init__(self, secrets_path: Optional[Path] = None):
        self.secrets_path = secrets_path or DEFAULT_SECRETS_PATH
        self._secrets: dict[str, Any] = {}

    def load(self) -> None:
        if self.secrets_path.exists():
            with open(self.secrets_path) as f:
                self._secrets = json.load(f)
            self._validate()
        else:
            # Fallback to env-only mode
            self._secrets = {
                "apis": {
                    "foursquare": {
                        "api_key": os.getenv("FOURSQUARE_API_KEY"),
                        "rate_limit": int(os.getenv("FOURSQUARE_RATE_LIMIT", "95000")),
                        "endpoint": os.getenv("FOURSQUARE_ENDPOINT", "https://api.foursquare.com")
                    },
                    "tomtom": {"api_key": os.getenv("TOMTOM_API_KEY")},
                    "yelp": {"api_key": os.getenv("YELP_API_KEY")},
                    "vercel": {"token": os.getenv("VERCEL_TOKEN"), "project": os.getenv("VERCEL_PROJECT")},
                },
                "services": {
                    "stripe": {"secret_key": os.getenv("STRIPE_SECRET_KEY"), "price_id": os.getenv("STRIPE_PRICE_ID")}
                },
                "databases": {
                    "sqlite": {"path": os.getenv("DB_PATH", "businesses.db")}
                }
            }

    def _validate(self) -> None:
        if not validate:
            return
        try:
            schema = json.loads(Path(SCHEMA_PATH).read_text())
            validate(instance=self._secrets, schema=schema)
        except ValidationError as e:
            raise RuntimeError(f"Secrets schema validation failed: {e}")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        return self._secrets.get(section, {}).get(key, default)

    def get_api_key(self, service: str) -> Optional[str]:
        return self._secrets.get("apis", {}).get(service, {}).get("api_key")

    def rotate(self, service: str) -> bool:
        # Stub: integrate with provider rotation
        print(f"[secrets] Rotation requested for {service} — implement provider API")
        return False


__all__ = ["SecretsManager"]
