from libraries.repository.db_setup.base_config import BaseConfig
from typing import Any
import os
import json

class FileConfig(BaseConfig):
    """Load configuration from a JSON file (DBsetup.json by default)."""

    def __init__(self, file_name: str = "DBsetup.json"):
        self.file_name = file_name
        if os.path.isfile(self.file_name):
            with open(self.file_name, encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def get(self, key: str) -> Any:
        return self.data.get(key)
