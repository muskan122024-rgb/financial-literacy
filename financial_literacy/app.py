"""
app.py — Streamlit entry point

Renders the sidebar navigation and routes to each page module.
Run with:  streamlit run app.py
"""
import sys
import os

# Make the project root importable regardless of how Streamlit is launched
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

# Page imports
from pages.dashboard import show as show_dashboard
from pages.budget_planner import show as show_budget
from pages.add_expense import show as show_add_expense
from pages.view_expenses import show as show_view_expenses
from pages.spending_analysis import show as show_analysis
from pages.afford_this import show as show_afford
from pages.loan_explainer import show as show_loan
from pages.scholarship_advisor import show as show_scholarship
from pages.ai_assistant import show as show_ai

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Financial Literacy",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Sidebar navigation
# ------------------------------------------------------------------
PAGES = {
    "🏠 Dashboard": show_dashboard,
    "📊 Budget Planner": show_budget,
    "➕ Add Expense": show_add_expense,
    "📋 View Expenses": show_view_expenses,
    "📈 Spending Analysis": show_analysis,
    "🤔 Can I Afford This?": show_afford,
    "🏦 Loan Explainer": show_loan,
    "🎓 Scholarship Advisor": show_scholarship,
    "🤖 AI Financial Assistant": show_ai,
}

st.sidebar.title("💰 Financial Literacy")
st.sidebar.markdown("*Your student money guide*")
st.sidebar.markdown("---")

selection = st.sidebar.radio("Navigate to", list(PAGES.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.caption(
    "This app is for **educational purposes only** and does not constitute "
    "professional financial advice."
)

# ------------------------------------------------------------------
# Render selected page
# ------------------------------------------------------------------
PAGES[selection]()
