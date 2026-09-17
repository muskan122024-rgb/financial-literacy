"""
pages/ai_assistant.py

IBM Bob / AI Financial Assistant chat interface.
"""
from __future__ import annotations

import streamlit as st

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from services.financial_assistant import FinancialAssistant
from utils.exceptions import AIServiceError, DataStorageError

_DISCLAIMER = (
    "⚠️ **Disclaimer:** The AI assistant provides educational information only. "
    "It is not a certified financial advisor. Do not make major financial decisions "
    "based solely on AI responses. Verify important information from official sources."
)

_STARTER_QUESTIONS = [
    "What is the 50-30-20 budgeting rule?",
    "How can I save money as a college student?",
    "What is the difference between a need and a want?",
    "How does compound interest work?",
    "What is an education loan and how does it work?",
    "How do I start building an emergency fund on a student budget?",
    "What is a credit score and why does it matter?",
]


def show() -> None:
    st.title("🤖 AI Financial Assistant")
    st.markdown(
        "Ask any financial literacy question. The assistant explains concepts "
        "in simple, student-friendly language."
    )
    st.warning(_DISCLAIMER)

    assistant = FinancialAssistant()

    if assistant.is_stub():
        st.info(
            "🔌 **Offline Mode:** The AI assistant is running without a backend. "
            "To enable real AI responses, add your API credentials to a `.env` file "
            "(see `.env.example`). All other app features work normally."
        )

    # ------------------------------------------------------------------
    # Initialise chat history in session state
    # ------------------------------------------------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ------------------------------------------------------------------
    # Optional: include financial context
    # ------------------------------------------------------------------
    include_context = st.checkbox(
        "📊 Include my current budget & spending as context for the AI",
        value=True,
        help="When enabled, the AI can reference your actual budget and spending data.",
    )

    context_str: str | None = None
    if include_context:
        try:
            budget = BudgetManager().get_budget()
            expenses = ExpenseManager().get_all_expenses()
            if budget:
                summary = FinancialAnalyzer.spending_summary(budget, expenses)
                context_str = (
                    f"Monthly income: ₹{summary['monthly_income']:,.2f}, "
                    f"Savings goal: ₹{summary['savings_goal']:,.2f}, "
                    f"Available for spending: ₹{summary['available_for_spending']:,.2f}, "
                    f"Total spent so far: ₹{summary['total_spent']:,.2f}, "
                    f"Remaining: ₹{summary['remaining']:,.2f}, "
                    f"Spending by category: {summary['by_category']}."
                )
        except DataStorageError:
            pass

    # ------------------------------------------------------------------
    # Starter question buttons
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("💬 Suggested Questions")
    cols = st.columns(2)
    for i, q in enumerate(_STARTER_QUESTIONS):
        if cols[i % 2].button(q, key=f"starter_{i}", use_container_width=True):
            _send_message(q, context_str, assistant)

    # ------------------------------------------------------------------
    # Chat history display
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("Conversation")

    if not st.session_state.chat_history:
        st.caption("Your conversation will appear here.")
    else:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ------------------------------------------------------------------
    # Input box
    # ------------------------------------------------------------------
    user_input = st.chat_input(
        "Ask a financial question…",
        key="ai_chat_input",
    )
    if user_input:
        _send_message(user_input, context_str, assistant)

    # ------------------------------------------------------------------
    # Clear conversation button
    # ------------------------------------------------------------------
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()


def _send_message(
    question: str, context: str | None, assistant: FinancialAssistant
) -> None:
    """Add a user message, get AI response, update session state."""
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Get AI response
    try:
        response = assistant.ask(question, context=context)
    except AIServiceError as e:
        response = (
            f"⚠️ The AI service is currently unavailable: {e}\n\n"
            "Please check your API configuration in the `.env` file."
        )

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()
