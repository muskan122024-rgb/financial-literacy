"""
tests/conftest.py

Shared pytest fixtures and helpers.
"""
from __future__ import annotations

import json
import tempfile
from datetime import date
from pathlib import Path

import pytest

from models.budget import Budget
from models.expense import Expense
from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager


@pytest.fixture
def tmp_budget_file(tmp_path: Path) -> Path:
    return tmp_path / "budget.json"


@pytest.fixture
def tmp_expenses_file(tmp_path: Path) -> Path:
    return tmp_path / "expenses.json"


@pytest.fixture
def budget_manager(tmp_budget_file: Path) -> BudgetManager:
    return BudgetManager(budget_file=tmp_budget_file)


@pytest.fixture
def expense_manager(tmp_expenses_file: Path) -> ExpenseManager:
    return ExpenseManager(expenses_file=tmp_expenses_file)


@pytest.fixture
def sample_budget() -> Budget:
    return Budget(monthly_income=10000.0, savings_goal=2000.0)


@pytest.fixture
def sample_expenses() -> list[Expense]:
    return [
        Expense(
            id="1",
            amount=500.0,
            category="Food",
            description="Lunch",
            date=date(2024, 1, 5),
        ),
        Expense(
            id="2",
            amount=1500.0,
            category="Rent",
            description="Hostel fee",
            date=date(2024, 1, 1),
        ),
        Expense(
            id="3",
            amount=200.0,
            category="Food",
            description="Dinner",
            date=date(2024, 1, 6),
        ),
        Expense(
            id="4",
            amount=300.0,
            category="Travel",
            description="Bus pass",
            date=date(2024, 1, 2),
        ),
    ]
