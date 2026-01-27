"""Vacancy domain model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, order=False)
class Vacancy:
    """Represents a vacancy from HH.

    Salary comparison uses expected_salary = max(salary_from, salary_to).
    If both are present, the larger bound is preferred as a proxy for potential.
    If missing, defaults to 0.
    """

    title: str
    url: str
    salary_from: int
    salary_to: int
    currency: str
    requirement: str
    responsibility: str

    def __post_init__(self) -> None:
        self.title = self.__validate_title(self.title)
        self.url = self.__validate_url(self.url)
        self.salary_from, self.salary_to, self.currency = self.__validate_salary(
            self.salary_from, self.salary_to, self.currency
        )
        self.requirement = self.requirement or ""
        self.responsibility = self.responsibility or ""

    @staticmethod
    def __validate_title(title: str) -> str:
        if not title:
            raise ValueError("Название вакансии не может быть пустым")
        return title

    @staticmethod
    def __validate_url(url: str) -> str:
        if not url:
            raise ValueError("URL вакансии не может быть пустым")
        return url

    @staticmethod
    def __validate_salary(
        salary_from: int | None, salary_to: int | None, currency: str | None
    ) -> tuple[int, int, str]:
        default_currency = "RUR"
        safe_from = salary_from if isinstance(salary_from, int) and salary_from > 0 else 0
        safe_to = salary_to if isinstance(salary_to, int) and salary_to > 0 else 0
        safe_currency = currency or default_currency
        return safe_from, safe_to, safe_currency

    def _expected_salary(self) -> int:
        """Return expected salary as max of bounds."""
        return max(self.salary_from, self.salary_to)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._expected_salary() < other._expected_salary()

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._expected_salary() <= other._expected_salary()

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._expected_salary() > other._expected_salary()

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._expected_salary() >= other._expected_salary()

    def __eq__(self, other: Any) -> bool:  # type: ignore[override]
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._expected_salary() == other._expected_salary()

    @classmethod
    def cast_to_object_list(cls, raw: list[dict]) -> list["Vacancy"]:
        """Convert raw HH items to Vacancy objects."""
        vacancies: list[Vacancy] = []
        for item in raw:
            name = item.get("name") or ""
            url = item.get("alternate_url") or ""
            salary_block = item.get("salary") or {}
            salary_from = salary_block.get("from") if isinstance(salary_block, dict) else None
            salary_to = salary_block.get("to") if isinstance(salary_block, dict) else None
            currency = salary_block.get("currency") if isinstance(salary_block, dict) else None
            snippet = item.get("snippet") or {}
            requirement = snippet.get("requirement") or ""
            responsibility = snippet.get("responsibility") or ""
            vacancies.append(
                cls(
                    title=name,
                    url=url,
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    requirement=requirement,
                    responsibility=responsibility,
                )
            )
        return vacancies
