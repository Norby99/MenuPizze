from libraries.repository.db_setup.base_config import BaseConfig
import os
import json
from typing import Any, Optional

class EnvConfig(BaseConfig):
    """Load configuration from environment variables."""

    _JSON_FIELDS = {"pizze", "ingredienti", "aggiunte", "insalate", "menu-settimanale"}

    _MAPPING = {
        "languageSite": "DB_LANGUAGE_SITE",
        "restaurantName": "DB_RESTAURANT_NAME",
        "defaultLanguage": "DB_DEFAULT_LANGUAGE",
        "m_key": "DB_M_KEY",
        "pizze": "DB_PIZZE",
        "ingredienti": "DB_INGREDIENTI",
        "aggiunte": "DB_AGGIUNTE",
        "insalate": "DB_INSALATE",
        "menu-settimanale": "DB_MENU_SETTIMANALE",
    }

    def __init__(self):
        self.env = os.environ

    def _get_env(self, *names: str) -> Optional[str]:
        for n in names:
            value = self.env.get(n)
            if value is not None:
                return value
        return None

    def get(self, key: str) -> Any:
        env_name = self._MAPPING.get(key, key.upper())
        raw = self.env.get(env_name)

        if raw is None:
            return None

        if key in self._JSON_FIELDS:
            try:
                return json.loads(raw)
            except Exception:
                return [s.strip() for s in raw.split(",") if s.strip()]

        return raw
