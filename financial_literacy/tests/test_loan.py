"""
tests/test_loan.py

Unit tests for LoanCalculator service.
"""
from __future__ import annotations

import math

import pytest

from services.loan_calculator import LoanCalculator
from utils.exceptions import InvalidLoanError


@pytest.fixture
def calc() -> LoanCalculator:
    return LoanCalculator()


# ------------------------------------------------------------------
# Validation tests
# ------------------------------------------------------------------

class TestLoanValidation:
    def test_zero_principal_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError, match="greater than"):
            calc.calculate(0.0, 10.0, 12)

    def test_negative_principal_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError):
            calc.calculate(-1000.0, 10.0, 12)

    def test_negative_interest_rate_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError, match="negative"):
            calc.calculate(10000.0, -5.0, 12)

    def test_interest_rate_above_100_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError, match="100"):
            calc.calculate(10000.0, 150.0, 12)

    def test_zero_tenure_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError, match="1 month"):
            calc.calculate(10000.0, 10.0, 0)

    def test_negative_tenure_raises(self, calc: LoanCalculator):
        with pytest.raises(InvalidLoanError):
            calc.calculate(10000.0, 10.0, -6)


# ------------------------------------------------------------------
# EMI calculation tests
# ------------------------------------------------------------------

class TestLoanCalculation:
    def test_zero_interest_emi_equals_principal_divided_by_months(
        self, calc: LoanCalculator
    ):
        result = calc.calculate(12000.0, 0.0, 12)
        assert result["monthly_emi"] == pytest.approx(1000.0, abs=0.01)
        assert result["total_interest"] == pytest.approx(0.0, abs=0.01)

    def test_total_repayment_equals_emi_times_months(self, calc: LoanCalculator):
        result = calc.calculate(100000.0, 10.0, 24)
        assert result["total_repayment"] == pytest.approx(
            result["monthly_emi"] * result["tenure_months"], abs=1.0
        )

    def test_total_interest_equals_repayment_minus_principal(
        self, calc: LoanCalculator
    ):
        result = calc.calculate(50000.0, 12.0, 18)
        expected_interest = result["total_repayment"] - result["principal"]
        assert result["total_interest"] == pytest.approx(expected_interest, abs=1.0)

    def test_result_contains_disclaimer(self, calc: LoanCalculator):
        result = calc.calculate(10000.0, 8.0, 12)
        assert "disclaimer" in result
        assert len(result["disclaimer"]) > 0

    def test_higher_interest_means_higher_total_repayment(
        self, calc: LoanCalculator
    ):
        low = calc.calculate(100000.0, 5.0, 24)
        high = calc.calculate(100000.0, 15.0, 24)
        assert high["total_repayment"] > low["total_repayment"]

    def test_longer_tenure_means_lower_emi(self, calc: LoanCalculator):
        short = calc.calculate(100000.0, 10.0, 12)
        long_ = calc.calculate(100000.0, 10.0, 36)
        assert long_["monthly_emi"] < short["monthly_emi"]

    def test_longer_tenure_means_higher_total_interest(self, calc: LoanCalculator):
        short = calc.calculate(100000.0, 10.0, 12)
        long_ = calc.calculate(100000.0, 10.0, 36)
        assert long_["total_interest"] > short["total_interest"]

    def test_known_emi_value(self, calc: LoanCalculator):
        # Verified manually: P=100000, r=10%/year, n=12 → EMI ≈ ₹8,791.59
        result = calc.calculate(100000.0, 10.0, 12)
        assert result["monthly_emi"] == pytest.approx(8791.59, abs=1.0)

    def test_result_has_all_required_keys(self, calc: LoanCalculator):
        result = calc.calculate(10000.0, 10.0, 12)
        required = {
            "principal", "annual_interest_rate", "tenure_months",
            "monthly_emi", "total_repayment", "total_interest", "disclaimer"
        }
        assert required.issubset(result.keys())


# ------------------------------------------------------------------
# Explain terms
# ------------------------------------------------------------------

class TestLoanTermExplanations:
    def test_explain_terms_returns_all_key_concepts(self, calc: LoanCalculator):
        terms = calc.explain_terms()
        expected_keys = [
            "Principal",
            "Interest Rate",
            "EMI (Equated Monthly Instalment)",
            "Tenure",
            "Total Repayment",
            "Total Interest",
        ]
        for key in expected_keys:
            assert key in terms

    def test_each_explanation_is_non_empty(self, calc: LoanCalculator):
        terms = calc.explain_terms()
        for key, explanation in terms.items():
            assert explanation.strip(), f"Explanation for '{key}' is empty"
