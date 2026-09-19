#  AI Financial Literacy Assistant

An AI-powered financial assistant designed to help college students manage their money, understand financial concepts, and make informed financial decisions.

##  About the Project

Many college students start managing their finances independently but have limited knowledge about budgeting, expenses, loans, scholarships, and financial planning.

The **AI Financial Literacy Assistant** provides simple, student-friendly financial guidance using AI.

##  Problem Statement

College students often struggle to:

* Manage their monthly budget
* Track daily expenses
* Understand spending patterns
* Decide whether they can afford a purchase
* Understand loans, interest, and repayment
* Find and understand scholarship information

This lack of financial knowledge can lead to poor spending habits and financial decisions.

##  Our Solution

We are building an AI-powered financial assistant that helps students understand and manage their finances through a simple and interactive interface.

The system can help users with:

* 💵 Budget planning
* 🧾 Expense tracking
* 📊 Spending analysis
* 🛒 "Can I afford this?" analysis
* 💳 Loan and EMI guidance
* 🎓 Scholarship guidance
* 🤖 AI-based financial questions

##  IBM Bob

**IBM Bob** is used as the AI assistant in our project.

It helps students understand financial questions and provides simple, personalized financial guidance.

### IBM Bob Workflow

```text
Student
   ↓
Financial Question / Information
   ↓
Application
   ↓
IBM Bob
   ↓
AI Processing
   ↓
Personalized Response
   ↓
Student
```

For detailed information about how IBM Bob is used in this project, see:

 **[IBM Bob Technology Usage](IBM_BOB_USAGE.md)**

##  Key Features

### 1. 💵 Budget Planner

Helps students plan and manage their monthly budget based on their available money.

### 2. 🧾 Expense Tracker

Allows students to record and categorize their daily expenses.

### 3. 📊 Spending Analysis

Analyzes expenses and helps students understand their spending patterns.

### 4. 🛒 Can I Afford This?

Helps students evaluate a planned purchase based on their available budget and expenses.

### 5. 💳 Loan Assistant

Provides simple explanations of loans, interest, EMI, and repayment concepts.

### 6. 🎓 Scholarship Assistant

Provides guidance related to scholarships and helps students understand eligibility information.

### 7. 🤖 AI Financial Assistant

Allows students to ask financial literacy questions and receive easy-to-understand responses.

## 🛠️ Technology Stack

| Technology        | Purpose                           |
| ----------------- | --------------------------------- |
| **IBM Bob**       | AI-powered financial assistance   |
| **Python**        | Application development           |
| **Streamlit**     | User interface                    |
| **Pandas**        | Data processing and analysis      |
| **SQLite**        | Data storage                      |
| **Generative AI** | Conversational financial guidance |

##  Project Workflow

```text
                ┌──────────────┐
                │    Student   │
                └──────┬───────┘
                       ↓
             Enter Financial Data
                       ↓
             ┌──────────────────┐
             │ Budget & Expense │
             │     Analysis     │
             └────────┬─────────┘
                      ↓
                ┌──────────┐
                │ IBM Bob  │
                └────┬─────┘
                     ↓
          Personalized Guidance
                     ↓
             Better Decisions
```

##  Target Users

* College students
* University students
* Young adults beginning to manage their finances

##  Repository Structure

```text
financial-literacy/
│
├── README.md
├── IBM_BOB_USAGE.md
├── app.py
├── requirements.txt
│
├── data/
│
└── assets/
```

> The repository structure may change as development progresses.

##  Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kanishka-9892/financial-literacy.git
```

### 2. Open the project folder

```bash
cd financial-literacy
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

##  IBM Bob Documentation

A separate document is included in this repository:

**`IBM_BOB_USAGE.md`**

It explains:

* How IBM Bob is used
* IBM Bob's role in the project
* AI workflow
* Financial assistance features
* Development activities involving IBM Bob

##  GitHub Repository

**Public Repository:**
https://github.com/Kanishka-9892/financial-literacy

##  Project Objective

The objective of this project is to make **financial literacy simple, accessible, and student-friendly**.

We aim to help students develop better financial habits, understand their spending, manage their budgets, and make informed financial decisions.

##  Hackathon

**IBM Hackathon – AI for Financial Literacy**

**Theme:** FinTech + Generative AI + Financial Literacy

##  Disclaimer

This project is designed for **financial education and general guidance**. It does not replace professional financial advice.
