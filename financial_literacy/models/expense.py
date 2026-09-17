"""
models/expense.py

Defines the Expense data model.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


EXPENSE_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Rent",
    "Entertainment",
    "Other",
]


@dataclass
class Expense:
    """Represents a single student expense entry."""

    amount: float
    category: str
    description: str
    date: date
    id: str = field(default="")

    # ------------------------------------------------------------------
    # Serialisation helpers (used by ExpenseManager for JSON storage)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert the expense to a plain dictionary for JSON storage."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Reconstruct an Expense from a stored dictionary."""
        return cls(
            id=data.get("id", ""),
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            date=date.fromisoformat(data["date"]),
        )

    def __str__(self) -> str:
        return (
            f"[{self.date}] {self.category} — ₹{self.amount:.2f} ({self.description})"
        )
