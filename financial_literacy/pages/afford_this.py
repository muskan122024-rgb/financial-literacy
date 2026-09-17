"""
pages/afford_this.py

"Can I Afford This?" — compares an item's price with remaining budget.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from utils.exceptions import DataStorageError, InvalidAmountError
from utils.validators import validate_positive_amount, validate_not_empty


def show() -> None:
    st.title("🤔 Can I Afford This?")
    st.markdown(
        "Enter an item and its price to see how it fits in your budget. "
        "This tool gives you information to help **you** make your own decision."
    )

    bm = BudgetManager()
    em = ExpenseManager()

    try:
        budget = bm.get_budget()
        expenses = em.get_all_expenses()
    except DataStorageError as e:
        st.error(f"Could not load data: {e}")
        return

    if budget is None:
        st.warning("Please set your budget first in **Budget Planner**.")
        return

    remaining = FinancialAnalyzer.remaining_budget(budget, expenses)

    # Show current remaining budget
    st.metric("💰 Your Current Remaining Budget", f"₹{remaining:,.2f}")
    st.markdown("---")

    # ------------------------------------------------------------------
    # Input form
    # ------------------------------------------------------------------
    with st.form("afford_form"):
        item_name = st.text_input(
            "Item Name",
            placeholder="e.g. New headphones",
            max_chars=100,
        )
        item_price = st.number_input(
            "Item Price (₹)",
            min_value=0.0,
            step=50.0,
            format="%.2f",
        )
        submitted = st.form_submit_button("📊 Check Affordability", type="primary")

    if submitted:
        try:
            validate_not_empty(item_name, "Item name")
            validate_positive_amount(item_price, "Item price")
        except (InvalidAmountError, Exception) as e:
            st.error(f"❌ {e}")
            return

        result = FinancialAnalyzer.affordability_check(item_name, item_price, remaining)

        st.markdown("---")
        st.subheader("📊 Affordability Check Result")

        col1, col2, col3 = st.columns(3)
        col1.metric("🛒 Item Price", f"₹{result['item_price']:,.2f}")
        col2.metric("💰 Budget Before", f"₹{result['remaining_before']:,.2f}")
        col3.metric(
            "💳 Budget After Purchase",
            f"₹{result['remaining_after']:,.2f}",
            delta=f"₹{result['remaining_after'] - result['remaining_before']:,.2f}",
            delta_color="inverse",
        )

        st.markdown("---")

        if result["can_cover"]:
            st.success("✅ Your budget can cover this item.")
        else:
            st.error("❌ This item costs more than your remaining budget.")

        st.info(f"💬 {result['impact_message']}")

        # ------------------------------------------------------------------
        # Educational guidance (always shown)
        # ------------------------------------------------------------------
        st.markdown("---")
        st.subheader("Things to consider before deciding:")
        st.markdown(
            """
            - **Is this a need or a want?** Essential expenses (food, rent, transport)
              should take priority over discretionary purchases.
            - **Does it affect your savings goal?** Even if you can afford it technically,
              would buying it compromise your monthly savings plan?
            - **Are there upcoming essential expenses?** Bills, tuition, or travel costs
              coming up may need that budget space.
            - **Is there a cheaper alternative?** Could you borrow, rent, or find a
              second-hand option?

            *This tool does not make financial decisions for you. The decision is yours.*
            """
        )
