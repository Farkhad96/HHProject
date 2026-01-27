from src.models.vacancy import Vacancy
from src.utils.filters import (
    filter_by_keywords,
    filter_by_salary_range,
    sort_vacancies,
    get_top_n,
)


def _vacancy(salary_from: int, salary_to: int, req: str = "", resp: str = "") -> Vacancy:
    return Vacancy(
        title="Dev",
        url=f"{salary_from}-{salary_to}",
        salary_from=salary_from,
        salary_to=salary_to,
        currency="RUR",
        requirement=req,
        responsibility=resp,
    )


def test_filter_by_keywords():
    vacancies = [
        _vacancy(0, 0, req="Python developer"),
        _vacancy(0, 0, req="Java"),
    ]
    result = filter_by_keywords(vacancies, ["python"])
    assert len(result) == 1
    assert result[0].requirement == "Python developer"


def test_filter_by_salary_range():
    vacancies = [_vacancy(100, 200), _vacancy(300, 400)]
    result = filter_by_salary_range(vacancies, 150, 350)
    assert len(result) == 1
    assert result[0].salary_from == 100


def test_sort_and_top():
    vacancies = [_vacancy(100, 200), _vacancy(50, 60), _vacancy(500, 0)]
    sorted_list = sort_vacancies(vacancies)
    assert sorted_list[0]._expected_salary() >= sorted_list[1]._expected_salary()
    top1 = get_top_n(sorted_list, 1)
    assert len(top1) == 1
    assert top1[0] == sorted_list[0]

