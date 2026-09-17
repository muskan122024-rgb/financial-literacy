"""
pages/loan_explainer.py

Educational loan section — explains terminology and estimates EMI.
"""
from __future__ import annotations

import streamlit as st

from services.loan_calculator import LoanCalculator
from utils.exceptions import InvalidLoanError


def show() -> None:
    st.title("🏦 Loan Explainer")
    st.markdown(
        "Learn how loans work and estimate monthly repayments. "
        "**All calculations are estimates for educational purposes only.**"
    )

    calc = LoanCalculator()

    # ------------------------------------------------------------------
    # Terminology section
    # ------------------------------------------------------------------
    with st.expander("📚 What do these loan terms mean?", expanded=True):
        terms = calc.explain_terms()
        for term, explanation in terms.items():
            st.markdown(f"**{term}**")
            st.caption(explanation)
            st.markdown("")

    st.markdown("---")

    # ------------------------------------------------------------------
    # EMI calculator form
    # ------------------------------------------------------------------
    st.subheader("📱 EMI Estimator")
    st.caption(
        "Enter your loan details below to see an estimated repayment breakdown."
    )

    with st.form("loan_form"):
        principal = st.number_input(
            "Loan Amount (₹)",
            min_value=0.0,
            step=1000.0,
            format="%.2f",
            help="The total amount you want to borrow.",
        )

        annual_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            format="%.2f",
            help="The yearly interest rate offered by the lender.",
        )

        tenure_months = st.number_input(
            "Loan Tenure (months)",
            min_value=1,
            max_value=360,
            value=12,
            step=1,
            help="How many months will you take to repay the loan?",
        )

        submitted = st.form_submit_button("📊 Calculate EMI", type="primary")

    if submitted:
        try:
            result = calc.calculate(principal, annual_rate, int(tenure_months))
        except InvalidLoanError as e:
            st.error(f"❌ {e}")
            return

        st.markdown("---")
        st.subheader("📊 Loan Breakdown")

        col1, col2 = st.columns(2)
        col1.metric("💰 Loan Amount (Principal)", f"₹{result['principal']:,.2f}")
        col2.metric("📅 Tenure", f"{result['tenure_months']} months")

        col3, col4, col5 = st.columns(3)
        col3.metric("📆 Monthly EMI", f"₹{result['monthly_emi']:,.2f}")
        col4.metric("💸 Total Repayment", f"₹{result['total_repayment']:,.2f}")
        col5.metric("📈 Total Interest Paid", f"₹{result['total_interest']:,.2f}")

        # Plain language explanation
        st.markdown("---")
        st.markdown(
            f"""
            **What this means in simple terms:**

            - You borrow **₹{result['principal']:,.2f}** at **{result['annual_interest_rate']}% per year**.
            - Every month, you pay **₹{result['monthly_emi']:,.2f}** for **{result['tenure_months']} months**.
            - By the end, you will have paid back a total of **₹{result['total_repayment']:,.2f}**.
            - Out of that, **₹{result['total_interest']:,.2f}** is the cost of borrowing
              (the interest you pay to the lender).
            """
        )

        st.warning(result["disclaimer"])

    # ------------------------------------------------------------------
    # General loan advice
    # ------------------------------------------------------------------
    st.markdown("---")
    with st.expander("💡 Things to know before taking a loan"):
        st.markdown(
            """
            - **Compare lenders.** Interest rates vary significantly between banks and
              NBFCs. Always compare before choosing.
            - **Read the fine print.** Check for processing fees, prepayment penalties,
              and other charges beyond the stated interest rate.
            - **Borrow only what you need.** A higher loan means higher EMIs and
              more interest paid overall.
            - **Longer tenure = smaller EMI, but more interest.** Choose a tenure
              that balances affordable EMIs with minimising total interest.
            - **Verify current rates with your bank.** Interest rates change. The
              figure you enter here may differ from actual rates at any given time.

            *For education loans in India, check the National Scholarship Portal
            (scholarships.gov.in) and your bank's official website for current schemes.*
            """
        )
