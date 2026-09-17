financial_literacy/
│
├── app.py                        ← Streamlit entry point, sidebar nav
│
├── models/
│   ├── __init__.py
│   ├── expense.py                ← Expense dataclass
│   └── budget.py                 ← Budget dataclass
│
├── services/
│   ├── __init__.py
│   ├── expense_manager.py        ← CRUD + CSV persistence for expenses
│   ├── budget_manager.py         ← CRUD + JSON persistence for budget
│   ├── financial_analyzer.py     ← Spending analysis, category stats
│   ├── loan_calculator.py        ← EMI formula, loan breakdown
│   └── financial_assistant.py    ← AI backend stub + prompt builder
│
├── utils/
│   ├── __init__.py
│   ├── validators.py             ← Pure validation functions
│   └── exceptions.py            ← Custom exception classes
│
├── pages/
│   ├── dashboard.py
│   ├── budget_planner.py
│   ├── add_expense.py
│   ├── view_expenses.py
│   ├── spending_analysis.py
│   ├── afford_this.py
│   ├── loan_explainer.py
│   ├── scholarship_advisor.py
│   └── ai_assistant.py
│
├── data/                         ← Auto-created at runtime
│   ├── expenses.json
│   └── budget.json
│
├── tests/
│   ├── __init__.py
│   ├── test_budget.py
│   ├── test_expense.py
│   ├── test_analyzer.py
│   └── test_loan.py
│
├── requirements.txt
├── .env.example
└── README.md
