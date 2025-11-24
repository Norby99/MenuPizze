import os
import json
from typing import Any, Optional


class _BaseConfig:
    """Small protocol for config sources."""

    def get(self, key: str) -> Any:
        raise NotImplementedError()


class FileConfig(_BaseConfig):
    """Load configuration from a JSON file (DBsetup.json by default)."""

    def __init__(self, file_name: str = "DBsetup.json"):
        self.file_name = file_name
        self.data = {}
        if os.path.isfile(self.file_name):
            with open(self.file_name, encoding="utf-8") as f:
                self.data = json.load(f)

    def get(self, key: str) -> Any:
        return self.data.get(key)


class EnvConfig(_BaseConfig):
    """Read configuration from environment variables.

    This class is tolerant: for each logical key it will try several
    environment variable names (with and without DB_ prefix). For list-like
    fields it will try to parse JSON; if that fails it will split on commas.
    """

    _JSON_FIELDS = {"pizze", "ingredienti", "aggiunte", "insalate", "menu-settimanale"}

    def __init__(self):
        self.env = os.environ

    def _get_env(self, *names: str) -> Optional[str]:
        for n in names:
            v = self.env.get(n)
            if v is not None:
                return v
        return None

    def get(self, key: str) -> Any:
        # mapping of logical keys to possible environment variable names
        mapping = {
            "languageSite": ("DB_LANGUAGE_SITE", "LANGUAGE_SITE", "languageSite"),
            "restaurantName": ("DB_RESTAURANT_NAME", "RESTAURANT_NAME", "restaurantName"),
            "defaultLanguage": ("DB_DEFAULT_LANGUAGE", "DEFAULT_LANGUAGE", "defaultLanguage"),
            "m_key": ("DB_M_KEY", "M_KEY", "m_key"),
            "pizze": ("DB_PIZZE", "PIZZE", "pizze"),
            "ingredienti": ("DB_INGREDIENTI", "INGREDIENTI", "ingredienti"),
            "aggiunte": ("DB_AGGIUNTE", "AGGIUNTE", "aggiunte"),
            "insalate": ("DB_INSALATE", "INSALATE", "insalate"),
            "menu-settimanale": ("DB_MENU_SETTIMANALE", "MENU_SETTIMANALE", "menu-settimanale"),
        }

        names = mapping.get(key, (key.upper(),))
        raw = self._get_env(*names)
        if raw is None:
            return None

        if key in self._JSON_FIELDS:
            # try parse JSON first (accept arrays/objects), otherwise allow
            # comma-separated lists as a fallback
            try:
                return json.loads(raw)
            except Exception:
                return [s.strip() for s in raw.split(",") if s.strip()]

        return raw


class DataReader:
    """Public API compatible with the previous implementation.

    Behavior:
    - If the JSON file (DBsetup.json) exists, read from it.
    - Otherwise read from environment variables. Environment variable names
      are tried with and without a DB_ prefix; list fields may be JSON or
      comma-separated strings.

    Assumptions:
    - Environment variables used (examples): DB_LANGUAGE_SITE, DB_RESTAURANT_NAME,
      DB_DEFAULT_LANGUAGE, DB_M_KEY, DB_PIZZE (JSON array or comma-separated),
      DB_INGREDIENTI, DB_AGGIUNTE, DB_INSALATE, DB_MENU_SETTIMANALE
    """

    def __init__(self, file_name: str = "DBsetup.json"):
        self.file_name = file_name
        if os.path.isfile(self.file_name):
            self.config = FileConfig(self.file_name)
            self.use_env = False
        else:
            self.config = EnvConfig()
            self.use_env = True

    def getWebsite(self) -> Optional[str]:
        language = self.config.get("languageSite")
        name = self.config.get("restaurantName")
        if language and name:
            return f"{language}/{name}.php"
        return None

    def getDefaultLanguage(self) -> Any:
        return self.config.get("defaultLanguage")

    def getToken(self) -> Any:
        return self.config.get("m_key")

    def getPizze(self) -> Any:
        return self.config.get("pizze")

    def getIngredienti(self) -> Any:
        return self.config.get("ingredienti")

    def getAggiunte(self) -> Any:
        return self.config.get("aggiunte")

    def getInsalate(self) -> Any:
        return self.config.get("insalate")

    def getMenuSettimanale(self) -> Any:
        return self.config.get("menu-settimanale")

