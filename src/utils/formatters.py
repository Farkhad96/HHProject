"""Human-readable formatting helpers."""

from __future__ import annotations

from src.models.vacancy import Vacancy


def format_vacancy(v: Vacancy) -> str:
    """Format a single vacancy for CLI output."""
    salary_part = f"{v.salary_from}-{v.salary_to} {v.currency}" if v.salary_from or v.salary_to else "Зарплата не указана"
    return (
        f"{v.title}\n"
        f"URL: {v.url}\n"
        f"Зарплата: {salary_part}\n"
        f"Требования: {v.requirement}\n"
        f"Обязанности: {v.responsibility}"
    )


def print_vacancies(vacancies: list[Vacancy]) -> None:
    """Print list of vacancies to stdout in human-readable form."""
    if not vacancies:
        print("Вакансии не найдены")
        return
    for vacancy in vacancies:
        print(format_vacancy(vacancy))
        print("-" * 40)

