"""Filtering and sorting utilities for vacancies."""

from __future__ import annotations

from typing import Iterable

from src.models.vacancy import Vacancy


def filter_by_keywords(vacancies: list[Vacancy], words: list[str]) -> list[Vacancy]:
    """Filter vacancies by presence of any keyword in requirement or responsibility."""
    lowered = [w.lower() for w in words]
    result: list[Vacancy] = []
    for vacancy in vacancies:
        haystack = f"{vacancy.requirement} {vacancy.responsibility}".lower()
        if any(word in haystack for word in lowered):
            result.append(vacancy)
    return result


def filter_by_salary_range(
    vacancies: list[Vacancy], min_salary: int, max_salary: int
) -> list[Vacancy]:
    """Filter vacancies where expected salary is within [min, max]."""
    result: list[Vacancy] = []
    for vacancy in vacancies:
        expected = vacancy._expected_salary()
        if min_salary <= expected <= max_salary:
            result.append(vacancy)
    return result


def sort_vacancies(vacancies: list[Vacancy], descending: bool = True) -> list[Vacancy]:
    """Sort vacancies by expected salary."""
    return sorted(vacancies, key=lambda v: v._expected_salary(), reverse=descending)


def get_top_n(vacancies: Iterable[Vacancy], n: int) -> list[Vacancy]:
    """Return top N vacancies from iterable."""
    return list(vacancies)[:n]

