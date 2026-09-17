"""
tests/test_analyzer.py

Unit tests for FinancialAnalyzer service.
"""
from __future__ import annotations

from datetime import date

import pytest

from models.budget import Budget
from models.expense import Expense
from services.financial_analyzer import FinancialAnalyzer


def make_expense(amount: float, category: str = "Food") -> Expense:
    return Expense(
        id="test",
        amount=amount,
        category=category,
        description="test",
        date=date.today(),
    )


# ------------------------------------------------------------------
# Total expenses
# ------------------------------------------------------------------

class TestTotalExpenses:
    def test_total_is_sum_of_all_amounts(self):
        expenses = [make_expense(100), make_expense(200), make_expense(300)]
        assert FinancialAnalyzer.total_expenses(expenses) == 600.0

    def test_total_with_no_expenses_is_zero(self):
        assert FinancialAnalyzer.total_expenses([]) == 0.0

    def test_total_with_single_expense(self):
        assert FinancialAnalyzer.total_expenses([make_expense(450.0)]) == 450.0


# ------------------------------------------------------------------
# Remaining budget
# ------------------------------------------------------------------

class TestRemainingBudget:
    def test_remaining_when_under_budget(self, sample_budget: Budget):
        # available = 8000, spent = 2500 → remaining = 5500
        expenses = [make_expense(1000), make_expense(1500)]
        remaining = FinancialAnalyzer.remaining_budget(sample_budget, expenses)
        assert remaining == 5500.0

    def test_remaining_when_no_expenses(self, sample_budget: Budget):
        # available = 8000, spent = 0 → remaining = 8000
        remaining = FinancialAnalyzer.remaining_budget(sample_budget, [])
        assert remaining == 8000.0

    def test_remaining_when_exactly_at_budget(self, sample_budget: Budget):
        # available = 8000, spent = 8000 → remaining = 0
        expenses = [make_expense(8000)]
        remaining = FinancialAnalyzer.remaining_budget(sample_budget, expenses)
        assert remaining == 0.0

    def test_remaining_is_negative_when_overspent(self, sample_budget: Budget):
        # available = 8000, spent = 9000 → remaining = -1000
        expenses = [make_expense(9000)]
        remaining = FinancialAnalyzer.remaining_budget(sample_budget, expenses)
        assert remaining == -1000.0


# ------------------------------------------------------------------
# Category breakdown
# ------------------------------------------------------------------

class TestSpendingByCategory:
    def test_groups_by_category(self):
        expenses = [
            make_expense(500, "Food"),
            make_expense(300, "Travel"),
            make_expense(200, "Food"),
        ]
        by_cat = FinancialAnalyzer.spending_by_category(expenses)
        assert by_cat["Food"] == 700.0
        assert by_cat["Travel"] == 300.0

    def test_empty_expenses_returns_empty_dict(self):
        assert FinancialAnalyzer.spending_by_category([]) == {}

    def test_single_category(self):
        expenses = [make_expense(100, "Education"), make_expense(200, "Education")]
        by_cat = FinancialAnalyzer.spending_by_category(expenses)
        assert by_cat == {"Education": 300.0}


# ------------------------------------------------------------------
# Spending percentage
# ------------------------------------------------------------------

class TestSpendingPercentage:
    def test_percentages_sum_to_100(self):
        expenses = [
            make_expense(600, "Food"),
            make_expense(300, "Travel"),
            make_expense(100, "Entertainment"),
        ]
        pct = FinancialAnalyzer.spending_percentage_by_category(expenses)
        assert abs(sum(pct.values()) - 100.0) < 0.01

    def test_single_category_is_100_percent(self):
        expenses = [make_expense(500, "Rent")]
        pct = FinancialAnalyzer.spending_percentage_by_category(expenses)
        assert pct["Rent"] == pytest.approx(100.0)

    def test_empty_expenses_returns_empty_dict(self):
        pct = FinancialAnalyzer.spending_percentage_by_category([])
        assert pct == {}


# ------------------------------------------------------------------
# Highest spending category
# ------------------------------------------------------------------

class TestHighestSpendingCategory:
    def test_returns_correct_highest_category(self):
        expenses = [
            make_expense(200, "Food"),
            make_expense(1500, "Rent"),
            make_expense(100, "Travel"),
        ]
        assert FinancialAnalyzer.highest_spending_category(expenses) == "Rent"

    def test_returns_none_for_empty_list(self):
        assert FinancialAnalyzer.highest_spending_category([]) is None


# ------------------------------------------------------------------
# "Can I Afford This?" logic
# ------------------------------------------------------------------

class TestAffordabilityCheck:
    def test_can_afford_when_remaining_greater_than_price(self):
        result = FinancialAnalyzer.affordability_check("Headphones", 500.0, 2000.0)
        assert result["can_cover"] is True
        assert result["remaining_after"] == 1500.0

    def test_cannot_afford_when_price_exceeds_remaining(self):
        result = FinancialAnalyzer.affordability_check("Laptop", 20000.0, 5000.0)
        assert result["can_cover"] is False
        assert result["remaining_after"] == -15000.0

    def test_exact_remaining_budget_is_affordable(self):
        result = FinancialAnalyzer.affordability_check("Book", 1000.0, 1000.0)
        assert result["can_cover"] is True
        assert result["remaining_after"] == 0.0

    def test_result_contains_required_keys(self):
        result = FinancialAnalyzer.affordability_check("Phone", 3000.0, 5000.0)
        required_keys = {
            "item_name", "item_price", "remaining_before",
            "remaining_after", "can_cover", "impact_message"
        }
        assert required_keys.issubset(result.keys())

    def test_impact_message_is_not_a_decision(self):
        result = FinancialAnalyzer.affordability_check("Shoes", 800.0, 2000.0)
        msg = result["impact_message"].lower()
        # Must not make a decision for the user
        assert "you should buy" not in msg
        assert "you should not buy" not in msg
        assert "do not buy" not in msg

    def test_zero_remaining_shows_correct_shortfall_info(self):
        result = FinancialAnalyzer.affordability_check("Jacket", 500.0, 0.0)
        assert result["can_cover"] is False
        assert result["remaining_after"] == -500.0


# ------------------------------------------------------------------
# Spending summary
# ------------------------------------------------------------------

class TestSpendingSummary:
    def test_summary_contains_required_keys(
        self, sample_budget: Budget, sample_expenses: list
    ):
        summary = FinancialAnalyzer.spending_summary(sample_budget, sample_expenses)
        required = {
            "monthly_income", "savings_goal", "available_for_spending",
            "total_spent", "remaining", "spent_percentage",
            "by_category", "percentage_by_category",
            "highest_spending_category", "is_overspent",
        }
        assert required.issubset(summary.keys())

    def test_summary_is_overspent_flag(self, sample_budget: Budget):
        # Spend more than available (8000)
        expenses = [make_expense(10000, "Rent")]
        summary = FinancialAnalyzer.spending_summary(sample_budget, expenses)
        assert summary["is_overspent"] is True

    def test_summary_not_overspent_flag(self, sample_budget: Budget):
        expenses = [make_expense(1000, "Food")]
        summary = FinancialAnalyzer.spending_summary(sample_budget, expenses)
        assert summary["is_overspent"] is False

    def test_summary_with_no_expenses(self, sample_budget: Budget):
        summary = FinancialAnalyzer.spending_summary(sample_budget, [])
        assert summary["total_spent"] == 0.0
        assert summary["remaining"] == sample_budget.available_for_spending
        assert summary["by_category"] == {}
