
from libraries.repository.db_setup.base_config import BaseConfig
from typing import Optional, Any
from libraries.repository.db_setup.base_config import BaseConfig
import os

class DataReader:
    """Reads configuration using a provided config source."""

    def __init__(self, config: BaseConfig = None, file_name="DBsetup.json"):
        self.config: BaseConfig = config or create_config(file_name)

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

def create_config(file_name: str = "DBsetup.json") -> BaseConfig:
    """Factory that returns FileConfig if file exists, otherwise EnvConfig."""
    if os.path.isfile(file_name):
        return FileConfig(file_name)
    return EnvConfig()
