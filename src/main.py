"""Console entrypoint for HH.ru vacancy CLI."""

from __future__ import annotations

from src.api.hh import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_saver import JSONSaver
from src.utils.filters import (
    filter_by_keywords,
    filter_by_salary_range,
    sort_vacancies,
    get_top_n,
)
from src.utils.formatters import print_vacancies


def _parse_salary_range(raw: str) -> tuple[int, int] | None:
    """Parse salary range like "100000-150000" into tuple; return None if empty."""
    if not raw:
        return None
    if "-" not in raw:
        raise ValueError("Диапазон зарплат должен быть в формате min-max")
    parts = raw.split("-", maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Диапазон зарплат должен быть в формате min-max")
    try:
        min_salary = int(parts[0])
        max_salary = int(parts[1])
    except ValueError as exc:  # noqa: BLE001
        raise ValueError("Значения зарплат должны быть числами") from exc
    if min_salary < 0 or max_salary < 0 or min_salary > max_salary:
        raise ValueError("Диапазон зарплат некорректен")
    return min_salary, max_salary


def user_interaction() -> None:
    """Main interactive flow: fetch, store, filter, sort, display vacancies."""
    api_client = HeadHunterAPI()
    storage = JSONSaver()

    keyword = input("Введите поисковый запрос: ").strip()
    if not keyword:
        print("Поисковый запрос не может быть пустым")
        return

    top_n_raw = input("Введите число вакансий для вывода (топ N): ").strip()
    if not top_n_raw.isdigit() or int(top_n_raw) <= 0:
        print("Топ N должно быть положительным числом")
        return
    top_n = int(top_n_raw)

    words_raw = input("Ключевые слова для фильтрации (через пробел, можно пусто): ").strip()
    words = [w for w in words_raw.split() if w]

    salary_range_raw = input(
        "Диапазон зарплат (например 100000-150000, можно пусто): "
    ).strip()
    try:
        salary_range = _parse_salary_range(salary_range_raw)
    except ValueError as exc:
        print(f"Ошибка ввода: {exc}")
        return

    try:
        raw_vacancies = api_client.get_vacancies(keyword)
    except Exception as exc:  # noqa: BLE001
        print(f"Не удалось получить вакансии: {exc}")
        return

    vacancies = Vacancy.cast_to_object_list(raw_vacancies)

    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    filtered = vacancies
    if words:
        filtered = filter_by_keywords(filtered, words)
    if salary_range:
        filtered = filter_by_salary_range(filtered, *salary_range)

    sorted_vacancies = sort_vacancies(filtered)
    top_vacancies = get_top_n(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

