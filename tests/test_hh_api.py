from types import SimpleNamespace

import pytest
import requests

from src.api.hh import HeadHunterAPI


class DummyResponse:
    def __init__(self, status_code: int = 200, json_data=None, text: str = "") -> None:
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def json(self):  # noqa: D401
        """Return prepared JSON data."""
        return self._json_data


def test_hh_api_params(monkeypatch):
    captured = {}

    def fake_get(url, params=None, timeout=None):  # noqa: ANN001
        captured["url"] = url
        captured["params"] = params
        return DummyResponse(status_code=200, json_data={"items": []})

    monkeypatch.setattr(requests, "get", fake_get)
    api = HeadHunterAPI()
    api.get_vacancies("python")
    assert captured["params"]["text"] == "python"
    assert captured["params"]["per_page"] == 100
    assert captured["params"]["area"] == 113


def test_hh_api_non_200(monkeypatch):
    def fake_get(url, params=None, timeout=None):  # noqa: ANN001
        return DummyResponse(status_code=500, text="err")

    monkeypatch.setattr(requests, "get", fake_get)
    api = HeadHunterAPI()
    with pytest.raises(ConnectionError):
        api.get_vacancies("python")


def test_hh_api_bad_json(monkeypatch):
    class BadResponse(DummyResponse):
        def json(self):  # noqa: D401
            """Raise ValueError to simulate bad JSON."""
            raise ValueError("bad json")

    def fake_get(url, params=None, timeout=None):  # noqa: ANN001
        return BadResponse(status_code=200)

    monkeypatch.setattr(requests, "get", fake_get)
    api = HeadHunterAPI()
    with pytest.raises(ValueError):
        api.get_vacancies("python")

