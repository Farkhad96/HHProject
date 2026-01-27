"""HeadHunter API client implementation."""

from __future__ import annotations

from typing import Any

import requests

from src.api.base import APIClient


class HeadHunterAPI(APIClient):
    """HeadHunter API client using requests."""

    __vacancies_endpoint: str
    __per_page: int
    __area: int

    def __init__(self, base_url: str = "https://api.hh.ru") -> None:
        super().__init__(base_url)
        self.__vacancies_endpoint = "/vacancies"
        self.__per_page = 100
        self.__area = 113

    def __connect(self) -> None:
        """Check availability of HH API."""
        super()._check_connection()

    def get_vacancies(self, keyword: str) -> list[dict]:
        """Fetch vacancies by keyword from HH."""
        if not keyword:
            raise ValueError("Ключевое слово не может быть пустым")

        self.__connect()

        url = f"{self._get_base_url()}{self.__vacancies_endpoint}"
        params = {
            "text": keyword,
            "per_page": self.__per_page,
            "area": self.__area,
        }
        try:
            response = requests.get(url, params=params, timeout=15)
        except requests.RequestException as exc:  # noqa: BLE001
            raise ConnectionError(f"Ошибка сети: {exc}") from exc

        if response.status_code != 200:
            raise ConnectionError(
                f"Ошибка ответа HH: {response.status_code} {response.text}"
            )

        try:
            data: dict[str, Any] = response.json()
        except ValueError as exc:  # noqa: BLE001
            raise ValueError("Некорректный JSON ответ от HH") from exc

        items = data.get("items")
        if not isinstance(items, list):
            raise ValueError("Ответ HH не содержит списка items")
        return items
