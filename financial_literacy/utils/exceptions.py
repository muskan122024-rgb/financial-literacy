"""
utils/exceptions.py

Custom exception hierarchy for the Financial Literacy application.
All exceptions inherit from FinancialLiteracyError so callers can
catch the base class when a broad handler is needed.
"""


class FinancialLiteracyError(Exception):
    """Base exception for the Financial Literacy application."""


class InvalidAmountError(FinancialLiteracyError):
    """Raised when a monetary amount is invalid (e.g. negative or zero)."""


class InvalidBudgetError(FinancialLiteracyError):
    """Raised when budget values are inconsistent or invalid."""


class InvalidExpenseError(FinancialLiteracyError):
    """Raised when an expense entry fails validation."""


class InvalidLoanError(FinancialLiteracyError):
    """Raised when loan parameters are invalid."""


class DataStorageError(FinancialLiteracyError):
    """Raised when reading from or writing to storage fails."""


class AIServiceError(FinancialLiteracyError):
    """Raised when the AI backend is unreachable or returns an error."""
