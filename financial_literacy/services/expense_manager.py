"""
services/expense_manager.py

Handles CRUD operations for expense entries.
Persistence: data/expenses.json
"""
from __future__ import annotations

import json
import uuid
from datetime import date
from pathlib import Path
from typing import List

from models.expense import Expense
from utils.exceptions import DataStorageError, InvalidExpenseError
from utils.validators import (
    validate_not_empty,
    validate_positive_amount,
    validate_date_string,
)

DATA_DIR = Path(__file__).parent.parent / "data"
EXPENSES_FILE = DATA_DIR / "expenses.json"


class ExpenseManager:
    """Manages expense entries: add, list, delete, persist."""

    def __init__(self, expenses_file: Path = EXPENSES_FILE) -> None:
        self._expenses_file = expenses_file
        self._ensure_data_dir()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        expense_date: date | str,
    ) -> Expense:
        """
        Validate and persist a new expense.
        Returns the saved Expense object.
        """
        validated_amount = validate_positive_amount(amount, "Expense amount")
        validated_category = validate_not_empty(category, "Category")
        validated_description = validate_not_empty(description, "Description")
        validated_date = validate_date_string(expense_date, "Expense date")

        expense = Expense(
            id=str(uuid.uuid4()),
            amount=validated_amount,
            category=validated_category,
            description=validated_description,
            date=validated_date,
        )

        expenses = self.get_all_expenses()
        expenses.append(expense)
        self._save(expenses)
        return expense

    def get_all_expenses(self) -> List[Expense]:
        """Load all expenses from disk. Returns empty list if none saved."""
        if not self._expenses_file.exists():
            return []
        try:
            with open(self._expenses_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            raise DataStorageError(
                f"Expenses file is corrupted or unreadable: {exc}"
            ) from exc

    def delete_expense(self, expense_id: str) -> bool:
        """
        Remove an expense by its ID.
        Returns True if deleted, False if not found.
        """
        expenses = self.get_all_expenses()
        filtered = [e for e in expenses if e.id != expense_id]
        if len(filtered) == len(expenses):
            return False
        self._save(filtered)
        return True

    def reset(self) -> None:
        """Delete all expenses (clears the expenses file)."""
        if self._expenses_file.exists():
            self._expenses_file.unlink()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _save(self, expenses: List[Expense]) -> None:
        try:
            with open(self._expenses_file, "w", encoding="utf-8") as fh:
                json.dump([e.to_dict() for e in expenses], fh, indent=2)
        except OSError as exc:
            raise DataStorageError(f"Could not save expenses: {exc}") from exc

    def _ensure_data_dir(self) -> None:
        self._expenses_file.parent.mkdir(parents=True, exist_ok=True)
