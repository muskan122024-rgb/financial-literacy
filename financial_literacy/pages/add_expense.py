"""
pages/add_expense.py

Form to add a new expense entry.
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from models.expense import EXPENSE_CATEGORIES
from services.expense_manager import ExpenseManager
from utils.exceptions import DataStorageError, InvalidExpenseError


def show() -> None:
    st.title("➕ Add Expense")
    st.markdown("Record a new expense to keep track of where your money is going.")

    em = ExpenseManager()

    with st.form("add_expense_form", clear_on_submit=True):
        st.subheader("New Expense")

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0,
            format="%.2f",
            help="How much did you spend?",
        )

        category = st.selectbox(
            "Category",
            options=EXPENSE_CATEGORIES,
            help="Select the category that best describes this expense.",
        )

        description = st.text_input(
            "Description",
            max_chars=200,
            placeholder="e.g. Lunch at college canteen",
            help="A short note about this expense.",
        )

        expense_date = st.date_input(
            "Date",
            value=date.today(),
            max_value=date.today(),
            help="The date of the expense. Cannot be in the future.",
        )

        submitted = st.form_submit_button("💾 Save Expense", type="primary")

    if submitted:
        try:
            expense = em.add_expense(
                amount=amount,
                category=category,
                description=description,
                expense_date=expense_date,
            )
            st.success(
                f"✅ Expense saved: **{expense.category}** — "
                f"₹{expense.amount:.2f} on {expense.date}"
            )
        except (InvalidExpenseError, ValueError) as e:
            st.error(f"❌ {e}")
        except DataStorageError as e:
            st.error(f"❌ Could not save expense: {e}")
