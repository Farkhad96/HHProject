import pytest

from src.models.vacancy import Vacancy


def test_salary_none_defaults_to_zero():
    vacancy = Vacancy(
        title="Dev",
        url="http://example.com",
        salary_from=None,
        salary_to=None,
        currency=None,
        requirement="",
        responsibility="",
    )
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0
    assert vacancy.currency == "RUR"


def test_comparison_by_expected_salary():
    a = Vacancy(
        title="A",
        url="1",
        salary_from=100,
        salary_to=200,
        currency="RUR",
        requirement="",
        responsibility="",
    )
    b = Vacancy(
        title="B",
        url="2",
        salary_from=50,
        salary_to=60,
        currency="RUR",
        requirement="",
        responsibility="",
    )
    assert a > b
    assert b < a
    assert a >= b
    assert b <= a
    assert not a == b

