"""
models/budget.py

Defines the Budget data model.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Budget:
    """Represents a student's monthly budget plan."""

    monthly_income: float
    savings_goal: float

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def available_for_spending(self) -> float:
        """Money available to spend after setting aside savings."""
        return self.monthly_income - self.savings_goal

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert budget to a plain dictionary for JSON storage."""
        return {
            "monthly_income": self.monthly_income,
            "savings_goal": self.savings_goal,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        """Reconstruct a Budget from a stored dictionary."""
        return cls(
            monthly_income=float(data["monthly_income"]),
            savings_goal=float(data["savings_goal"]),
        )

    def __str__(self) -> str:
        return (
            f"Budget — Income: ₹{self.monthly_income:.2f}, "
            f"Savings Goal: ₹{self.savings_goal:.2f}, "
            f"Available: ₹{self.available_for_spending:.2f}"
        )
