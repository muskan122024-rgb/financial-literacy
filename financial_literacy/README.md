# 💰 AI for Financial Literacy

A beginner-friendly student financial literacy application built with Python, Streamlit, and IBM Bob.

> **Disclaimer:** This application is for **educational purposes only**. It does not constitute professional financial advice. Always verify important financial decisions with a qualified advisor or official sources.

---

## 🎯 What Does This App Do?

Helps college students understand and manage their personal finances through:

| Feature | Description |
|---|---|
| 📊 Budget Planner | Set monthly income and savings goal |
| ➕ Add Expense | Record expenses by category, description, and date |
| 📋 View Expenses | See all recorded expenses with totals |
| 📈 Spending Analysis | Category-wise spending breakdown and insights |
| 🤔 Can I Afford This? | Check if an item fits your remaining budget |
| 🏦 Loan Explainer | Learn loan concepts and estimate EMI |
| 🎓 Scholarship Advisor | Get guidance on scholarship criteria and documents |
| 🤖 AI Financial Assistant | Chat with IBM Bob for financial literacy help |

---

## 📁 Project Structure

```
financial_literacy/
│
├── app.py                        ← Streamlit entry point
│
├── models/
│   ├── expense.py                ← Expense dataclass
│   └── budget.py                 ← Budget dataclass
│
├── services/
│   ├── budget_manager.py         ← Budget CRUD + JSON persistence
│   ├── expense_manager.py        ← Expense CRUD + JSON persistence
│   ├── financial_analyzer.py     ← Spending analysis (pure logic)
│   ├── loan_calculator.py        ← EMI formula and loan breakdown
│   └── financial_assistant.py   ← AI backend abstraction
│
├── utils/
│   ├── validators.py             ← Input validation functions
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
│   ├── expenses.json             ← Stored expense entries
│   └── budget.json               ← Stored budget settings
│
├── tests/
│   ├── test_budget.py
│   ├── test_expense.py
│   ├── test_analyzer.py
│   └── test_loan.py
│
├── requirements.txt
├── .env.example                  ← Template for AI credentials
└── README.md
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone <your-repo-url>
cd financial_literacy
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` installs:
- `streamlit` — the web UI framework
- `pytest` — for running tests
- `python-dotenv` — for loading `.env` credentials
- `requests` — for making AI API calls

---

## 🔑 Configuring IBM Bob / AI Credentials (Optional)

The app works fully **without AI credentials** — the AI assistant runs in a safe offline stub mode.

To enable real AI responses:

### Step 1: Copy the example file

```bash
cp .env.example .env
```

### Step 2: Edit `.env` with your credentials

```
# For WatsonX / IBM Generative AI
AI_BACKEND=watsonx
AI_API_URL=https://your-watsonx-endpoint/v1/generate
AI_API_KEY=your-api-key-here
AI_MODEL_ID=ibm/granite-13b-instruct-v2

# OR for OpenAI-compatible endpoint
AI_BACKEND=openai
AI_API_URL=https://api.openai.com/v1
AI_API_KEY=your-openai-key-here
AI_MODEL_ID=gpt-3.5-turbo
```

### ⚠️ Important security rules:
- **Never** commit your `.env` file to Git
- **Never** hardcode API keys in source code
- The `.env` file is already in `.gitignore`

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

Expected output: **76 tests, all passing.**

To run a specific test file:

```bash
python -m pytest tests/test_budget.py -v
python -m pytest tests/test_expense.py -v
python -m pytest tests/test_analyzer.py -v
python -m pytest tests/test_loan.py -v
```

---

## 🔢 EMI Calculation Formula

The loan calculator uses the standard **reducing-balance EMI formula**:

```
EMI = P × r × (1 + r)^n
      ──────────────────
         (1 + r)^n - 1

Where:
  P = Principal (loan amount)
  r = Monthly interest rate = Annual rate / 12 / 100
  n = Tenure in months
```

If interest rate is 0%, EMI = Principal ÷ Tenure.

---

## 🤖 AI Assistant — How It Works

The `FinancialAssistant` class uses an environment-variable-driven backend:

| `AI_BACKEND` value | What happens |
|---|---|
| `stub` (default) | Safe offline mode, no API call |
| `openai` | Calls OpenAI-compatible chat completions API |
| `watsonx` | Calls IBM WatsonX text generation API |

The AI is always given this system prompt:

> *"You are a student financial literacy assistant. Your role is to explain financial concepts clearly and help students understand their options. Do not present yourself as a financial advisor. Do not make decisions for the user. Do not fabricate current scholarship, loan, interest-rate, or government-program information..."*

---

## 📊 Data Storage

- **`data/budget.json`** — stores monthly income and savings goal
- **`data/expenses.json`** — stores all expense entries (array of objects)

No sensitive data is stored. The app does **not** store passwords, bank account numbers, card numbers, UPI PINs, or API keys.

---

## ⚠️ Limitations

1. **Single-user app** — all data is for one student on one machine. No login, no multi-user support.
2. **Monthly scope only** — the app tracks one budget period at a time. Use "Reset All Data" to start a new month.
3. **AI requires credentials** — without a `.env` file, the AI assistant shows a stub response. All other features work fully.
4. **Scholarship information is general** — the app gives guidance about what to look for. Always verify eligibility from official sources like [scholarships.gov.in](https://scholarships.gov.in).
5. **Loan calculations are estimates** — actual EMI and repayment may differ based on your lender's terms.

---

## 🏫 For Hackathon Presenters

Here is a simple explanation of the app's architecture for your presentation:

1. **Models** (`models/`) — define what data looks like (a Budget has income and savings; an Expense has amount, category, date)
2. **Services** (`services/`) — handle the business logic (calculating EMI, analyzing spending, talking to the AI)
3. **Pages** (`pages/`) — each Streamlit page is one Python file with a `show()` function
4. **Utils** (`utils/`) — reusable validation and exception classes used across the app
5. **Tests** (`tests/`) — 76 pytest tests that verify every calculation and validation rule

---

*Built as a college hackathon project. For educational purposes only.*
