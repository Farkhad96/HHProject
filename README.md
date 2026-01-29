# HH.ru Vacancy CLI

Console tool to fetch vacancies from HH.ru, store them in JSON, and filter/sort/show them.

## Requirements
- Python 3.11+
- `requests`
- Optional: `pytest`, `pytest-cov`

## Installation
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -e .[dev]
```

## Usage
```bash
python -m src.main
```
Follow the prompts: keyword, top N, keywords filter, salary range (e.g. `100000-150000`).

## Tests
```bash
pytest
```

## Notes
- Data is stored in `vacancies.json` in the project root.
- HeadHunter API is used via plain `requests`.

