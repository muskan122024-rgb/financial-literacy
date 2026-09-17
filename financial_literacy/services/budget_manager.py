"""
services/budget_manager.py

Handles reading and writing the student's budget plan.
Persistence: data/budget.json
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from models.budget import Budget
from utils.exceptions import DataStorageError, InvalidBudgetError
from utils.validators import validate_income, validate_savings_goal

DATA_DIR = Path(__file__).parent.parent / "data"
BUDGET_FILE = DATA_DIR / "budget.json"


class BudgetManager:
    """Manages the student's monthly budget (save, load, reset)."""

    def __init__(self, budget_file: Path = BUDGET_FILE) -> None:
        self._budget_file = budget_file
        self._ensure_data_dir()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_budget(self, monthly_income: float, savings_goal: float) -> Budget:
        """
        Validate and persist a new budget.
        Returns the saved Budget object.
        """
        income = validate_income(monthly_income)
        savings = validate_savings_goal(savings_goal, income)
        budget = Budget(monthly_income=income, savings_goal=savings)
        self._save(budget)
        return budget

    def get_budget(self) -> Budget | None:
        """
        Load the budget from disk.
        Returns None if no budget has been set yet.
        """
        if not self._budget_file.exists():
            return None
        try:
            with open(self._budget_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return Budget.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            raise DataStorageError(
                f"Budget file is corrupted or unreadable: {exc}"
            ) from exc

    def reset(self) -> None:
        """Delete the budget file (clears the saved budget)."""
        if self._budget_file.exists():
            self._budget_file.unlink()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _save(self, budget: Budget) -> None:
        try:
            with open(self._budget_file, "w", encoding="utf-8") as fh:
                json.dump(budget.to_dict(), fh, indent=2)
        except OSError as exc:
            raise DataStorageError(f"Could not save budget: {exc}") from exc

    def _ensure_data_dir(self) -> None:
        self._budget_file.parent.mkdir(parents=True, exist_ok=True)
