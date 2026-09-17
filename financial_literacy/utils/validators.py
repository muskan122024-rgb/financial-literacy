"""
utils/validators.py

Pure validation functions — no Streamlit imports, no side effects.
Each function raises the appropriate custom exception on failure and
returns the (possibly coerced) value on success.
"""
from __future__ import annotations

from datetime import date, datetime

from utils.exceptions import (
    InvalidAmountError,
    InvalidBudgetError,
    InvalidExpenseError,
    InvalidLoanError,
)


def validate_positive_amount(value: float, field_name: str = "Amount") -> float:
    """Ensure a monetary value is strictly greater than zero."""
    if value is None:
        raise InvalidAmountError(f"{field_name} is required.")
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise InvalidAmountError(f"{field_name} must be a number.")
    if value <= 0:
        raise InvalidAmountError(f"{field_name} must be greater than ₹0.")
    return value


def validate_non_negative(value: float, field_name: str = "Value") -> float:
    """Ensure a value is zero or positive."""
    if value is None:
        raise InvalidAmountError(f"{field_name} is required.")
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise InvalidAmountError(f"{field_name} must be a number.")
    if value < 0:
        raise InvalidAmountError(f"{field_name} cannot be negative.")
    return value


def validate_not_empty(value: str, field_name: str = "Field") -> str:
    """Ensure a string field is not blank."""
    if not value or not str(value).strip():
        raise InvalidExpenseError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_date_string(value: str | date, field_name: str = "Date") -> date:
    """
    Accept a date object or an ISO-format string (YYYY-MM-DD).
    Returns a date object. Future dates are rejected.
    """
    if isinstance(value, date):
        parsed = value
    else:
        try:
            parsed = datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
        except ValueError:
            raise InvalidExpenseError(
                f"{field_name} must be a valid date in YYYY-MM-DD format."
            )
    if parsed > date.today():
        raise InvalidExpenseError(f"{field_name} cannot be in the future.")
    return parsed


def validate_income(monthly_income: float) -> float:
    """Validate monthly income."""
    try:
        monthly_income = float(monthly_income)
    except (TypeError, ValueError):
        raise InvalidBudgetError("Monthly income must be a number.")
    if monthly_income <= 0:
        raise InvalidBudgetError("Monthly income must be greater than ₹0.")
    return monthly_income


def validate_savings_goal(savings_goal: float, monthly_income: float) -> float:
    """Validate savings goal relative to monthly income."""
    try:
        savings_goal = float(savings_goal)
    except (TypeError, ValueError):
        raise InvalidBudgetError("Savings goal must be a number.")
    if savings_goal < 0:
        raise InvalidBudgetError("Savings goal cannot be negative.")
    if savings_goal > monthly_income:
        raise InvalidBudgetError(
            f"Savings goal (₹{savings_goal:.2f}) cannot exceed "
            f"monthly income (₹{monthly_income:.2f})."
        )
    return savings_goal


def validate_loan_amount(amount: float) -> float:
    """Validate loan principal."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise InvalidLoanError("Loan amount must be a number.")
    if amount <= 0:
        raise InvalidLoanError("Loan amount must be greater than ₹0.")
    return amount


def validate_interest_rate(rate: float) -> float:
    """Validate annual interest rate (0–100 %)."""
    try:
        rate = float(rate)
    except (TypeError, ValueError):
        raise InvalidLoanError("Interest rate must be a number.")
    if rate < 0:
        raise InvalidLoanError("Interest rate cannot be negative.")
    if rate > 100:
        raise InvalidLoanError("Interest rate cannot exceed 100%.")
    return rate


def validate_tenure(months: int) -> int:
    """Validate loan tenure in months."""
    try:
        months = int(months)
    except (TypeError, ValueError):
        raise InvalidLoanError("Loan tenure must be a whole number of months.")
    if months <= 0:
        raise InvalidLoanError("Loan tenure must be at least 1 month.")
    return months
