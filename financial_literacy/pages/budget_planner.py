"""
pages/budget_planner.py

Allows the student to set their monthly income and savings goal.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from utils.exceptions import DataStorageError, InvalidBudgetError


def show() -> None:
    st.title("📊 Budget Planner")
    st.markdown(
        "Set your monthly income and savings goal. "
        "The app will calculate how much you have available to spend."
    )

    bm = BudgetManager()

    # Load existing budget to pre-fill the form
    try:
        existing = bm.get_budget()
    except DataStorageError:
        existing = None

    current_income = existing.monthly_income if existing else 0.0
    current_savings = existing.savings_goal if existing else 0.0

    # ------------------------------------------------------------------
    # Form
    # ------------------------------------------------------------------
    with st.form("budget_form"):
        st.subheader("Set Your Monthly Budget")

        monthly_income = st.number_input(
            "Monthly Available Money (₹)",
            min_value=0.0,
            value=current_income,
            step=100.0,
            format="%.2f",
            help="Enter the total money you receive or have available each month.",
        )

        savings_goal = st.number_input(
            "Savings Goal (₹)",
            min_value=0.0,
            value=current_savings,
            step=100.0,
            format="%.2f",
            help="How much do you want to save this month? (Cannot exceed income.)",
        )

        submitted = st.form_submit_button("💾 Save Budget", type="primary")

    if submitted:
        try:
            budget = bm.set_budget(monthly_income, savings_goal)
            st.success("✅ Budget saved successfully!")
            st.markdown("---")

            col1, col2, col3 = st.columns(3)
            col1.metric("💵 Monthly Income", f"₹{budget.monthly_income:,.2f}")
            col2.metric("🎯 Savings Goal", f"₹{budget.savings_goal:,.2f}")
            col3.metric(
                "💳 Available for Spending",
                f"₹{budget.available_for_spending:,.2f}",
            )

            if budget.savings_goal == 0:
                st.info(
                    "💡 Tip: Setting a savings goal — even a small amount — helps "
                    "you build a financial safety net over time."
                )
        except InvalidBudgetError as e:
            st.error(f"❌ {e}")
        except DataStorageError as e:
            st.error(f"❌ Could not save budget: {e}")

    # ------------------------------------------------------------------
    # Display current budget if it exists
    # ------------------------------------------------------------------
    if existing and not submitted:
        st.markdown("---")
        st.subheader("Your Current Budget")
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Monthly Income", f"₹{existing.monthly_income:,.2f}")
        col2.metric("🎯 Savings Goal", f"₹{existing.savings_goal:,.2f}")
        col3.metric(
            "💳 Available for Spending",
            f"₹{existing.available_for_spending:,.2f}",
        )

    # ------------------------------------------------------------------
    # Educational note
    # ------------------------------------------------------------------
    st.markdown("---")
    with st.expander("💡 Why is budgeting important?"):
        st.markdown(
            """
            A budget helps you:
            - **Know where your money goes** — instead of wondering why it ran out.
            - **Prioritise savings** — saving first ensures you build a financial cushion.
            - **Avoid overspending** — you can see in advance if a purchase fits your plan.
            - **Reduce financial stress** — having a plan makes money feel more manageable.

            A simple rule many students find helpful is the **50-30-20 rule**:
            - 50% on needs (rent, food, transport)
            - 30% on wants (entertainment, shopping)
            - 20% on savings

            *This is a general guideline — adjust it to fit your own situation.*
            """
        )
