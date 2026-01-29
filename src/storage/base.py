"""Abstract storage interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.vacancy import Vacancy


class Storage(ABC):
    """Abstract storage for vacancies."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Add a vacancy to storage."""
        raise NotImplementedError

    @abstractmethod
    def get_vacancies(self, criteria: dict | None = None) -> list[Vacancy]:
        """Retrieve vacancies, optionally filtered by criteria."""
        raise NotImplementedError

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Delete a vacancy from storage."""
        raise NotImplementedError

