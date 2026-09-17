"""
pages/dashboard.py

Dashboard — shows a quick overview of budget and spending.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from utils.exceptions import DataStorageError


def show() -> None:
    st.title("🏠 Dashboard")
    st.markdown("Welcome! Here is a quick overview of your finances this month.")

    bm = BudgetManager()
    em = ExpenseManager()

    try:
        budget = bm.get_budget()
        expenses = em.get_all_expenses()
    except DataStorageError as e:
        st.error(f"Could not load data: {e}")
        return

    if budget is None:
        st.info(
            "👋 You haven't set a budget yet. "
            "Go to **Budget Planner** in the sidebar to get started."
        )
        return

    summary = FinancialAnalyzer.spending_summary(budget, expenses)

    # ------------------------------------------------------------------
    # Key metrics row
    # ------------------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Monthly Income", f"₹{summary['monthly_income']:,.2f}")
    col2.metric("🎯 Savings Goal", f"₹{summary['savings_goal']:,.2f}")
    col3.metric(
        "💳 Available for Spending",
        f"₹{summary['available_for_spending']:,.2f}",
    )

    st.markdown("---")

    col4, col5, col6 = st.columns(3)
    col4.metric("💸 Total Spent", f"₹{summary['total_spent']:,.2f}")

    remaining = summary["remaining"]
    delta_color = "normal" if remaining >= 0 else "inverse"
    col5.metric(
        "💰 Remaining Budget",
        f"₹{remaining:,.2f}",
        delta=f"{'Over budget' if remaining < 0 else 'Under budget'}",
        delta_color=delta_color,
    )
    col6.metric("📊 Spent %", f"{summary['spent_percentage']:.1f}%")

    # ------------------------------------------------------------------
    # Overspending alert
    # ------------------------------------------------------------------
    if summary["is_overspent"]:
        st.warning(
            f"⚠️ You have spent ₹{abs(remaining):,.2f} more than your available "
            "spending amount this month. Consider reviewing your expenses."
        )

    # ------------------------------------------------------------------
    # Category breakdown (bar chart)
    # ------------------------------------------------------------------
    if summary["by_category"]:
        st.markdown("---")
        st.subheader("Spending by Category")
        st.bar_chart(summary["by_category"])

        top = summary["highest_spending_category"]
        if top:
            pct = summary["percentage_by_category"].get(top, 0)
            st.caption(
                f"Your highest spending category is **{top}** "
                f"({pct:.1f}% of total spending)."
            )
    else:
        st.info("No expenses recorded yet. Add your first expense in **Add Expense**.")

    # ------------------------------------------------------------------
    # Reset button
    # ------------------------------------------------------------------
    st.markdown("---")
    with st.expander("⚠️ Danger Zone — Reset All Data"):
        st.warning(
            "This will permanently delete your budget and all expenses. "
            "This cannot be undone."
        )
        if st.button("🗑️ Reset All Data", type="primary"):
            bm.reset()
            em.reset()
            st.success("All data has been reset. You can now set a new budget.")
            st.rerun()
