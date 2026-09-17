"""
tests/test_budget.py

Unit tests for Budget model and BudgetManager service.
"""
from __future__ import annotations

import pytest

from models.budget import Budget
from services.budget_manager import BudgetManager
from utils.exceptions import InvalidBudgetError, DataStorageError


# ------------------------------------------------------------------
# Budget model tests
# ------------------------------------------------------------------

class TestBudgetModel:
    def test_available_for_spending_is_income_minus_savings(self):
        b = Budget(monthly_income=10000.0, savings_goal=2000.0)
        assert b.available_for_spending == 8000.0

    def test_available_for_spending_zero_savings(self):
        b = Budget(monthly_income=5000.0, savings_goal=0.0)
        assert b.available_for_spending == 5000.0

    def test_available_for_spending_savings_equals_income(self):
        b = Budget(monthly_income=5000.0, savings_goal=5000.0)
        assert b.available_for_spending == 0.0

    def test_to_dict_round_trip(self):
        b = Budget(monthly_income=12000.0, savings_goal=3000.0)
        recovered = Budget.from_dict(b.to_dict())
        assert recovered.monthly_income == b.monthly_income
        assert recovered.savings_goal == b.savings_goal

    def test_str_representation(self):
        b = Budget(monthly_income=10000.0, savings_goal=1000.0)
        assert "₹10000.00" in str(b)
        assert "₹1000.00" in str(b)


# ------------------------------------------------------------------
# Budget validation tests
# ------------------------------------------------------------------

class TestBudgetValidation:
    def test_valid_budget_is_accepted(self, budget_manager: BudgetManager):
        budget = budget_manager.set_budget(10000.0, 2000.0)
        assert budget.monthly_income == 10000.0
        assert budget.savings_goal == 2000.0

    def test_zero_income_raises(self, budget_manager: BudgetManager):
        with pytest.raises(InvalidBudgetError, match="greater than"):
            budget_manager.set_budget(0.0, 0.0)

    def test_negative_income_raises(self, budget_manager: BudgetManager):
        with pytest.raises(InvalidBudgetError):
            budget_manager.set_budget(-1000.0, 0.0)

    def test_negative_savings_raises(self, budget_manager: BudgetManager):
        with pytest.raises(InvalidBudgetError, match="negative"):
            budget_manager.set_budget(5000.0, -100.0)

    def test_savings_exceeds_income_raises(self, budget_manager: BudgetManager):
        with pytest.raises(InvalidBudgetError, match="cannot exceed"):
            budget_manager.set_budget(5000.0, 6000.0)

    def test_savings_equal_to_income_is_valid(self, budget_manager: BudgetManager):
        budget = budget_manager.set_budget(5000.0, 5000.0)
        assert budget.available_for_spending == 0.0

    def test_zero_savings_is_valid(self, budget_manager: BudgetManager):
        budget = budget_manager.set_budget(8000.0, 0.0)
        assert budget.savings_goal == 0.0

    def test_non_numeric_income_raises(self, budget_manager: BudgetManager):
        with pytest.raises(InvalidBudgetError):
            budget_manager.set_budget("abc", 0.0)  # type: ignore


# ------------------------------------------------------------------
# BudgetManager persistence tests
# ------------------------------------------------------------------

class TestBudgetManagerPersistence:
    def test_set_and_get_budget(self, budget_manager: BudgetManager):
        budget_manager.set_budget(10000.0, 2500.0)
        loaded = budget_manager.get_budget()
        assert loaded is not None
        assert loaded.monthly_income == 10000.0
        assert loaded.savings_goal == 2500.0

    def test_get_budget_returns_none_when_no_file(self, budget_manager: BudgetManager):
        result = budget_manager.get_budget()
        assert result is None

    def test_reset_removes_budget(self, budget_manager: BudgetManager):
        budget_manager.set_budget(10000.0, 1000.0)
        budget_manager.reset()
        assert budget_manager.get_budget() is None

    def test_set_budget_overwrites_previous(self, budget_manager: BudgetManager):
        budget_manager.set_budget(5000.0, 500.0)
        budget_manager.set_budget(12000.0, 3000.0)
        loaded = budget_manager.get_budget()
        assert loaded.monthly_income == 12000.0
        assert loaded.savings_goal == 3000.0
