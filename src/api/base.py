"""Abstract API client definition."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Final

import requests


class APIClient(ABC):
    """Abstract base for API clients."""

    __base_url: Final[str]

    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url.rstrip("/")

    def _get_base_url(self) -> str:
        """Protected accessor for base URL (read-only)."""
        return self.__base_url

    def _connect(self) -> None:
        """Check API availability with a GET request to base URL."""
        try:
            response = requests.get(self.__base_url, timeout=10)
        except requests.RequestException as exc:  # noqa: BLE001
            raise ConnectionError(f"Не удалось подключиться к API: {exc}") from exc
        if response.status_code != 200:
            raise ConnectionError(
                f"API недоступно, статус: {response.status_code}"
            )

    def _check_connection(self) -> None:
        """Template method to verify availability (used by children)."""
        self._connect()

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list[dict]:
        """Fetch vacancies for given keyword."""
        raise NotImplementedError
