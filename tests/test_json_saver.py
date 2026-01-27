import json
from pathlib import Path

import pytest

from src.models.vacancy import Vacancy
from src.storage.json_saver import JSONSaver


def test_add_and_prevent_duplicates(tmp_path: Path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONSaver(str(file_path))
    vacancy = Vacancy(
        title="Dev",
        url="http://example.com",
        salary_from=0,
        salary_to=0,
        currency="RUR",
        requirement="",
        responsibility="",
    )
    storage.add_vacancy(vacancy)
    storage.add_vacancy(vacancy)
    data = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(data) == 1


def test_delete_vacancy(tmp_path: Path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONSaver(str(file_path))
    vacancy1 = Vacancy(
        title="Dev1",
        url="http://example.com/1",
        salary_from=0,
        salary_to=0,
        currency="RUR",
        requirement="",
        responsibility="",
    )
    vacancy2 = Vacancy(
        title="Dev2",
        url="http://example.com/2",
        salary_from=0,
        salary_to=0,
        currency="RUR",
        requirement="",
        responsibility="",
    )
    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)
    storage.delete_vacancy(vacancy1)
    data = json.loads(file_path.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["url"] == vacancy2.url

