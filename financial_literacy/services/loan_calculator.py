"""
services/loan_calculator.py

Educational loan EMI calculator.
All results are estimates and clearly stated as such.
"""
from __future__ import annotations

import math

from utils.validators import validate_loan_amount, validate_interest_rate, validate_tenure


class LoanCalculator:
    """
    Calculates estimated EMI, total repayment, and total interest for a loan.

    Formula (standard reducing-balance EMI):
        EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)

    Where:
        P = principal
        r = monthly interest rate = annual_rate / 12 / 100
        n = tenure in months

    Special case: if interest rate is 0, EMI = principal / tenure.
    """

    DISCLAIMER = (
        "⚠️ These figures are estimates for educational purposes only. "
        "Actual loan terms, EMI, and repayment amounts will vary based on the "
        "lender's terms and conditions. Always verify with your bank or lender "
        "before making any financial decisions."
    )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def calculate(
        self,
        principal: float,
        annual_interest_rate: float,
        tenure_months: int,
    ) -> dict:
        """
        Validate inputs and return a loan breakdown dict containing:
          - principal
          - annual_interest_rate
          - tenure_months
          - monthly_emi
          - total_repayment
          - total_interest
          - disclaimer
        """
        p = validate_loan_amount(principal)
        r_annual = validate_interest_rate(annual_interest_rate)
        n = validate_tenure(tenure_months)

        emi = self._emi(p, r_annual, n)
        total_repayment = round(emi * n, 2)
        total_interest = round(total_repayment - p, 2)

        return {
            "principal": p,
            "annual_interest_rate": r_annual,
            "tenure_months": n,
            "monthly_emi": round(emi, 2),
            "total_repayment": total_repayment,
            "total_interest": total_interest,
            "disclaimer": self.DISCLAIMER,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _emi(principal: float, annual_rate: float, tenure_months: int) -> float:
        """Core EMI formula."""
        if annual_rate == 0:
            return principal / tenure_months
        r = annual_rate / 12 / 100
        emi = principal * r * math.pow(1 + r, tenure_months) / (
            math.pow(1 + r, tenure_months) - 1
        )
        return emi

    @staticmethod
    def explain_terms() -> dict:
        """Return plain-language definitions of loan terminology."""
        return {
            "Principal": (
                "The original amount of money you borrow from a bank or lender. "
                "For example, if you take a loan of ₹1,00,000, that is your principal."
            ),
            "Interest Rate": (
                "The percentage the lender charges you for borrowing money, "
                "usually expressed per year (annual rate). "
                "For example, 10% per annum means you pay 10% of the remaining "
                "loan amount as interest each year."
            ),
            "EMI (Equated Monthly Instalment)": (
                "The fixed monthly amount you pay to repay the loan. "
                "Each EMI covers part of the principal and part of the interest."
            ),
            "Tenure": (
                "The total period over which you repay the loan, measured in months. "
                "A longer tenure means smaller EMIs but more total interest paid."
            ),
            "Total Repayment": (
                "The total amount you pay back over the full loan period. "
                "This equals EMI × number of months."
            ),
            "Total Interest": (
                "Total Repayment minus the Principal. "
                "This is the actual cost of borrowing the money."
            ),
        }
