"""JSON storage implementation for vacancies."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.models.vacancy import Vacancy
from src.storage.base import Storage


class JSONSaver(Storage):
    """File-based storage for vacancies in JSON."""

    __filename: str

    def __init__(self, filename: str = "vacancies.json") -> None:
        self.__filename = filename
        self.__ensure_file()

    def __ensure_file(self) -> None:
        path = Path(self.__filename)
        if not path.exists():
            path.write_text("[]", encoding="utf-8")

    def __read(self) -> list[dict[str, Any]]:
        path = Path(self.__filename)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # noqa: BLE001
            raise ValueError("Некорректный формат файла хранения") from exc
        if not isinstance(data, list):
            raise ValueError("Ожидался список вакансий в файле хранения")
        return data

    def __write(self, data: list[dict[str, Any]]) -> None:
        path = Path(self.__filename)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Add vacancy to JSON storage, skipping duplicates by URL."""
        data = self.__read()
        if any(item.get("url") == vacancy.url for item in data):
            return
        data.append(asdict(vacancy))
        self.__write(data)

    def get_vacancies(self, criteria: dict | None = None) -> list[Vacancy]:
        """Return vacancies, optionally filtered by simple equality criteria."""
        data = self.__read()
        vacancies = [Vacancy(**item) for item in data]
        if not criteria:
            return vacancies
        filtered: list[Vacancy] = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if not hasattr(vacancy, key) or getattr(vacancy, key) != value:
                    match = False
                    break
            if match:
                filtered.append(vacancy)
        return filtered

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Delete vacancy by URL."""
        data = self.__read()
        new_data = [item for item in data if item.get("url") != vacancy.url]
        self.__write(new_data)
