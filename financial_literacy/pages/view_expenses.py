"""
pages/view_expenses.py

Lists all recorded expenses with totals.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from utils.exceptions import DataStorageError


def show() -> None:
    st.title("📋 View Expenses")
    st.markdown("All your recorded expenses for this month.")

    em = ExpenseManager()
    bm = BudgetManager()

    try:
        expenses = em.get_all_expenses()
        budget = bm.get_budget()
    except DataStorageError as e:
        st.error(f"Could not load data: {e}")
        return

    if not expenses:
        st.info("No expenses recorded yet. Add your first expense in **Add Expense**.")
        return

    # ------------------------------------------------------------------
    # Summary metrics
    # ------------------------------------------------------------------
    total = FinancialAnalyzer.total_expenses(expenses)
    col1, col2 = st.columns(2)
    col1.metric("💸 Total Spent", f"₹{total:,.2f}")

    if budget:
        remaining = FinancialAnalyzer.remaining_budget(budget, expenses)
        col2.metric(
            "💰 Remaining Budget",
            f"₹{remaining:,.2f}",
            delta="Over budget" if remaining < 0 else "Under budget",
            delta_color="inverse" if remaining < 0 else "normal",
        )
    else:
        col2.info("Set a budget to see remaining balance.")

    st.markdown("---")

    # ------------------------------------------------------------------
    # Expense table
    # ------------------------------------------------------------------
    st.subheader(f"Expenses ({len(expenses)} entries)")

    rows = []
    for e in sorted(expenses, key=lambda x: x.date, reverse=True):
        rows.append(
            {
                "Date": str(e.date),
                "Category": e.category,
                "Description": e.description,
                "Amount (₹)": f"₹{e.amount:,.2f}",
                "ID": e.id,
            }
        )

    import pandas as pd  # type: ignore
    df = pd.DataFrame(rows)
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)

    # ------------------------------------------------------------------
    # Delete an expense
    # ------------------------------------------------------------------
    st.markdown("---")
    with st.expander("🗑️ Delete an Expense"):
        expense_options = {
            f"[{e.date}] {e.category} — ₹{e.amount:.2f} — {e.description}": e.id
            for e in expenses
        }
        selected_label = st.selectbox(
            "Select expense to delete", list(expense_options.keys())
        )
        if st.button("Delete Selected Expense", type="secondary"):
            expense_id = expense_options[selected_label]
            try:
                deleted = em.delete_expense(expense_id)
                if deleted:
                    st.success("✅ Expense deleted.")
                    st.rerun()
                else:
                    st.warning("Expense not found — it may have already been deleted.")
            except DataStorageError as e:
                st.error(f"❌ {e}")
