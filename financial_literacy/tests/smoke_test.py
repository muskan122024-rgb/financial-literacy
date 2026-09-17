import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from services.budget_manager import BudgetManager
from services.expense_manager import ExpenseManager
from services.financial_analyzer import FinancialAnalyzer
from services.loan_calculator import LoanCalculator
from services.financial_assistant import FinancialAssistant
from datetime import date

# 1. Set budget
bm = BudgetManager()
b = bm.set_budget(15000, 3000)
print(f"[BUDGET] income={b.monthly_income} savings={b.savings_goal} available={b.available_for_spending}")

# 2. Add expenses
em = ExpenseManager()
em.reset()
e1 = em.add_expense(2000, "Food", "Monthly groceries", date.today())
e2 = em.add_expense(500, "Travel", "Bus pass", date.today())
e3 = em.add_expense(800, "Entertainment", "Movie and dinner", date.today())
print(f"[EXPENSES] added 3 expenses, total in file: {len(em.get_all_expenses())}")

# 3. Analysis
expenses = em.get_all_expenses()
total = FinancialAnalyzer.total_expenses(expenses)
remaining = FinancialAnalyzer.remaining_budget(b, expenses)
by_cat = FinancialAnalyzer.spending_by_category(expenses)
pct = FinancialAnalyzer.spending_percentage_by_category(expenses)
top = FinancialAnalyzer.highest_spending_category(expenses)
print(f"[ANALYSIS] total={total} remaining={remaining}")
print(f"[ANALYSIS] by_category={by_cat}")
print(f"[ANALYSIS] top_category={top}")

# 4. Can I Afford This
result = FinancialAnalyzer.affordability_check("New phone", 12000, remaining)
can_cover = result["can_cover"]
remaining_after = result["remaining_after"]
msg_snippet = result["impact_message"][:80]
print(f"[AFFORD] can_cover={can_cover} remaining_after={remaining_after}")
print(f"[AFFORD] message={msg_snippet}...")

# 5. Loan calculation
lc = LoanCalculator()
loan = lc.calculate(100000, 10.0, 24)
print(f"[LOAN] emi={loan['monthly_emi']} total={loan['total_repayment']} interest={loan['total_interest']}")

# 6. AI assistant stub
ai = FinancialAssistant()
is_stub = ai.is_stub()
resp = ai.ask("What is a budget?")
print(f"[AI] is_stub={is_stub}")
print(f"[AI] response snippet={resp[:60]}...")

# 7. Delete expense
deleted = em.delete_expense(e1.id)
count_after_delete = len(em.get_all_expenses())
print(f"[DELETE] deleted={deleted} remaining_count={count_after_delete}")

# 8. Reset
bm.reset()
em.reset()
budget_after = bm.get_budget()
expenses_after = em.get_all_expenses()
print(f"[RESET] budget_after_reset={budget_after} expenses_count_after_reset={len(expenses_after)}")

print("\nALL FLOWS PASSED")
