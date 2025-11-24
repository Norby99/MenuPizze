import os
from abc import ABC, abstractmethod
from typing import Any

class BaseConfig(ABC):
    """Interface for configuration sources."""

    @abstractmethod
    def get(self, key: str) -> Any:
        pass
