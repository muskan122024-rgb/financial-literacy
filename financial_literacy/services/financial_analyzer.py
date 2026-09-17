"""
services/financial_analyzer.py

Pure analysis logic — no storage, no Streamlit.
Receives a list of Expense objects and a Budget, produces summaries.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from models.budget import Budget
from models.expense import Expense


class FinancialAnalyzer:
    """
    Analyzes a student's expenses relative to their budget.
    All methods are pure (no side effects, no I/O).
    """

    # ------------------------------------------------------------------
    # Totals
    # ------------------------------------------------------------------

    @staticmethod
    def total_expenses(expenses: List[Expense]) -> float:
        """Sum of all expense amounts."""
        return sum(e.amount for e in expenses)

    @staticmethod
    def remaining_budget(budget: Budget, expenses: List[Expense]) -> float:
        """
        Money left after subtracting total expenses from available spending.
        Can be negative if the student has overspent.
        """
        return budget.available_for_spending - FinancialAnalyzer.total_expenses(
            expenses
        )

    # ------------------------------------------------------------------
    # Category breakdown
    # ------------------------------------------------------------------

    @staticmethod
    def spending_by_category(expenses: List[Expense]) -> Dict[str, float]:
        """Return a dict mapping category name → total amount spent."""
        result: Dict[str, float] = {}
        for expense in expenses:
            result[expense.category] = result.get(expense.category, 0.0) + expense.amount
        return result

    @staticmethod
    def spending_percentage_by_category(
        expenses: List[Expense],
    ) -> Dict[str, float]:
        """
        Return a dict mapping category → percentage of total spending.
        Returns empty dict if there are no expenses.
        """
        total = FinancialAnalyzer.total_expenses(expenses)
        if total == 0:
            return {}
        by_cat = FinancialAnalyzer.spending_by_category(expenses)
        return {cat: (amount / total) * 100 for cat, amount in by_cat.items()}

    @staticmethod
    def highest_spending_category(expenses: List[Expense]) -> Optional[str]:
        """Return the category with the most spending, or None if no expenses."""
        by_cat = FinancialAnalyzer.spending_by_category(expenses)
        if not by_cat:
            return None
        return max(by_cat, key=lambda c: by_cat[c])

    # ------------------------------------------------------------------
    # "Can I Afford This?" logic
    # ------------------------------------------------------------------

    @staticmethod
    def affordability_check(
        item_name: str,
        item_price: float,
        remaining: float,
    ) -> dict:
        """
        Evaluate whether an item can be afforded given remaining budget.

        Returns a dict with:
          - item_name
          - item_price
          - remaining_before
          - remaining_after
          - can_cover        True if remaining >= item_price
          - impact_message   Educational explanation (neutral, no decision)
        """
        remaining_after = remaining - item_price
        can_cover = remaining >= item_price

        if can_cover and remaining_after >= 0:
            impact = (
                f"Your remaining budget is ₹{remaining:.2f}. "
                f"Buying '{item_name}' for ₹{item_price:.2f} would leave you with "
                f"₹{remaining_after:.2f}. "
                "Before deciding, consider whether this is an essential expense, "
                "whether it affects your savings goal, and how it fits with your "
                "existing spending this month."
            )
        elif can_cover and remaining_after == 0:
            impact = (
                f"Buying '{item_name}' for ₹{item_price:.2f} would use your entire "
                f"remaining budget of ₹{remaining:.2f}. You would have ₹0.00 left. "
                "Think carefully about whether any other essential expenses are still "
                "coming up this month."
            )
        else:
            shortfall = abs(remaining_after)
            impact = (
                f"'{item_name}' costs ₹{item_price:.2f}, but your remaining budget is "
                f"only ₹{remaining:.2f}. You would be ₹{shortfall:.2f} over budget. "
                "Consider whether this purchase is essential right now, or whether it "
                "can wait until your next budget cycle."
            )

        return {
            "item_name": item_name,
            "item_price": item_price,
            "remaining_before": remaining,
            "remaining_after": remaining_after,
            "can_cover": can_cover,
            "impact_message": impact,
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    @staticmethod
    def spending_summary(budget: Budget, expenses: List[Expense]) -> dict:
        """
        Produce a complete snapshot suitable for display on the dashboard.
        """
        total_spent = FinancialAnalyzer.total_expenses(expenses)
        remaining = FinancialAnalyzer.remaining_budget(budget, expenses)
        by_cat = FinancialAnalyzer.spending_by_category(expenses)
        pct_by_cat = FinancialAnalyzer.spending_percentage_by_category(expenses)
        top_cat = FinancialAnalyzer.highest_spending_category(expenses)

        # Spending rate as % of available-for-spending
        if budget.available_for_spending > 0:
            spent_pct = (total_spent / budget.available_for_spending) * 100
        else:
            spent_pct = 0.0

        return {
            "monthly_income": budget.monthly_income,
            "savings_goal": budget.savings_goal,
            "available_for_spending": budget.available_for_spending,
            "total_spent": total_spent,
            "remaining": remaining,
            "spent_percentage": spent_pct,
            "by_category": by_cat,
            "percentage_by_category": pct_by_cat,
            "highest_spending_category": top_cat,
            "is_overspent": remaining < 0,
        }
