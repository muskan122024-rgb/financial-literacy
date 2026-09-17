"""
pages/spending_analysis.py

Displays category-wise spending analysis and tips.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from utils.exceptions import DataStorageError


def show() -> None:
    st.title("📈 Spending Analysis")
    st.markdown("Understand where your money is going this month.")

    bm = BudgetManager()
    em = ExpenseManager()

    try:
        budget = bm.get_budget()
        expenses = em.get_all_expenses()
    except DataStorageError as e:
        st.error(f"Could not load data: {e}")
        return

    if budget is None:
        st.info("Please set your budget first in **Budget Planner**.")
        return

    if not expenses:
        st.info("No expenses recorded yet. Add some expenses to see your analysis.")
        return

    summary = FinancialAnalyzer.spending_summary(budget, expenses)

    # ------------------------------------------------------------------
    # Overview metrics
    # ------------------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("💸 Total Spent", f"₹{summary['total_spent']:,.2f}")
    col2.metric("💰 Remaining", f"₹{summary['remaining']:,.2f}")
    col3.metric("📊 Spent %", f"{summary['spent_percentage']:.1f}%")

    if summary["is_overspent"]:
        st.error(
            f"⚠️ You have overspent by ₹{abs(summary['remaining']):,.2f} this month."
        )
    elif summary["spent_percentage"] >= 80:
        st.warning(
            "📢 You've used more than 80% of your available spending budget. "
            "Be mindful of remaining expenses this month."
        )
    else:
        st.success("✅ Your spending is within budget.")

    st.markdown("---")

    # ------------------------------------------------------------------
    # Category bar chart
    # ------------------------------------------------------------------
    st.subheader("Spending by Category")
    by_cat = summary["by_category"]
    pct_by_cat = summary["percentage_by_category"]

    st.bar_chart(by_cat)

    # ------------------------------------------------------------------
    # Category breakdown table
    # ------------------------------------------------------------------
    st.subheader("Category Breakdown")

    rows = []
    for cat, amount in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        rows.append(
            {
                "Category": cat,
                "Amount (₹)": f"₹{amount:,.2f}",
                "% of Total Spending": f"{pct_by_cat.get(cat, 0):.1f}%",
            }
        )

    import pandas as pd  # type: ignore
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ------------------------------------------------------------------
    # Insights
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("💡 Observations")

    top_cat = summary["highest_spending_category"]
    if top_cat:
        top_pct = pct_by_cat.get(top_cat, 0)
        st.info(
            f"Your highest spending category is **{top_cat}** "
            f"({top_pct:.1f}% of your total spending). "
            "Consider whether this reflects your actual priorities."
        )

    if len(by_cat) == 1:
        st.info(
            "All your expenses are in one category. "
            "Try adding more expense categories to get a fuller picture."
        )

    st.markdown(
        """
        **Tips for better spending habits:**
        - Review your top spending categories regularly.
        - Ask yourself: *Is this spending aligned with my goals?*
        - Small daily expenses (like coffee or snacks) can add up quickly.
        - Compare this month's spending to see if patterns are changing.

        *This analysis is for your personal awareness only and is not financial advice.*
        """
    )
