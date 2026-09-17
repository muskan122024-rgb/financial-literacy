"""
tests/test_expense.py

Unit tests for Expense model and ExpenseManager service.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from models.expense import Expense
from services.expense_manager import ExpenseManager
from utils.exceptions import InvalidExpenseError, DataStorageError


# ------------------------------------------------------------------
# Expense model tests
# ------------------------------------------------------------------

class TestExpenseModel:
    def test_to_dict_round_trip(self):
        e = Expense(
            id="abc",
            amount=450.0,
            category="Food",
            description="Lunch",
            date=date(2024, 6, 15),
        )
        recovered = Expense.from_dict(e.to_dict())
        assert recovered.id == e.id
        assert recovered.amount == e.amount
        assert recovered.category == e.category
        assert recovered.description == e.description
        assert recovered.date == e.date

    def test_str_contains_amount_and_category(self):
        e = Expense(
            id="x", amount=200.0, category="Travel",
            description="Bus", date=date(2024, 1, 1)
        )
        assert "Travel" in str(e)
        assert "200.00" in str(e)


# ------------------------------------------------------------------
# Expense validation tests
# ------------------------------------------------------------------

class TestExpenseValidation:
    def test_valid_expense_is_accepted(self, expense_manager: ExpenseManager):
        e = expense_manager.add_expense(
            amount=300.0,
            category="Food",
            description="Dinner",
            expense_date=date.today(),
        )
        assert e.amount == 300.0
        assert e.category == "Food"

    def test_zero_amount_raises(self, expense_manager: ExpenseManager):
        with pytest.raises(Exception, match="greater than"):
            expense_manager.add_expense(0.0, "Food", "Test", date.today())

    def test_negative_amount_raises(self, expense_manager: ExpenseManager):
        with pytest.raises(Exception):
            expense_manager.add_expense(-100.0, "Food", "Test", date.today())

    def test_empty_category_raises(self, expense_manager: ExpenseManager):
        with pytest.raises(Exception, match="empty"):
            expense_manager.add_expense(100.0, "   ", "Test", date.today())

    def test_empty_description_raises(self, expense_manager: ExpenseManager):
        with pytest.raises(Exception, match="empty"):
            expense_manager.add_expense(100.0, "Food", "", date.today())

    def test_future_date_raises(self, expense_manager: ExpenseManager):
        future = date.today() + timedelta(days=1)
        with pytest.raises(Exception, match="future"):
            expense_manager.add_expense(100.0, "Food", "Test", future)

    def test_today_date_is_valid(self, expense_manager: ExpenseManager):
        e = expense_manager.add_expense(50.0, "Food", "Snack", date.today())
        assert e.date == date.today()

    def test_past_date_is_valid(self, expense_manager: ExpenseManager):
        past = date(2023, 1, 1)
        e = expense_manager.add_expense(100.0, "Education", "Books", past)
        assert e.date == past


# ------------------------------------------------------------------
# ExpenseManager CRUD tests
# ------------------------------------------------------------------

class TestExpenseManagerCRUD:
    def test_add_expense_persists(self, expense_manager: ExpenseManager):
        expense_manager.add_expense(200.0, "Food", "Lunch", date.today())
        loaded = expense_manager.get_all_expenses()
        assert len(loaded) == 1
        assert loaded[0].amount == 200.0

    def test_multiple_expenses_persist(self, expense_manager: ExpenseManager):
        expense_manager.add_expense(100.0, "Food", "Breakfast", date.today())
        expense_manager.add_expense(500.0, "Rent", "Hostel", date.today())
        loaded = expense_manager.get_all_expenses()
        assert len(loaded) == 2

    def test_get_all_returns_empty_list_when_no_file(
        self, expense_manager: ExpenseManager
    ):
        result = expense_manager.get_all_expenses()
        assert result == []

    def test_delete_expense(self, expense_manager: ExpenseManager):
        e = expense_manager.add_expense(300.0, "Shopping", "Notebook", date.today())
        deleted = expense_manager.delete_expense(e.id)
        assert deleted is True
        remaining = expense_manager.get_all_expenses()
        assert len(remaining) == 0

    def test_delete_nonexistent_expense_returns_false(
        self, expense_manager: ExpenseManager
    ):
        result = expense_manager.delete_expense("nonexistent-id")
        assert result is False

    def test_reset_clears_all_expenses(self, expense_manager: ExpenseManager):
        expense_manager.add_expense(100.0, "Food", "Lunch", date.today())
        expense_manager.add_expense(200.0, "Travel", "Bus", date.today())
        expense_manager.reset()
        assert expense_manager.get_all_expenses() == []

    def test_each_expense_gets_unique_id(self, expense_manager: ExpenseManager):
        e1 = expense_manager.add_expense(100.0, "Food", "A", date.today())
        e2 = expense_manager.add_expense(200.0, "Travel", "B", date.today())
        assert e1.id != e2.id
