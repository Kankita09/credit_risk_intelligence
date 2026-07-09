# 📊 Credit Risk Intelligence

> An end-to-end data analysis project for predicting home loan default risk — built with Python, Streamlit, and AI-powered insights.

🔗 **Live Dashboard**: [creditriskintelligence.streamlit.app](https://creditriskintelligence.streamlit.app)

---

## 📌 Project Overview

Credit Risk Intelligence is a complete data analytics solution built on the **Home Credit Default Risk** dataset from Kaggle. The project covers the full data analyst lifecycle — from raw data ingestion and cleaning, through exploratory analysis and feature engineering, to an interactive dashboard and an AI-powered assistant that answers business questions in plain English.

The goal is to help financial institutions identify high-risk loan applicants early, understand the factors driving default, and make more informed credit decisions.

---

## 🗂️ Dataset

**Source**: [Home Credit Default Risk — Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk)

| Detail | Value |
|---|---|
| Raw files used | 5 CSVs (application_train, bureau, previous_application, installments_payments, credit_card_balance) |
| Final merged dataset | `app_final.csv` |
| Rows | 307,511 |
| Columns (after cleaning) | 75 |
| Target variable | `TARGET` — 1 = defaulted, 0 = repaid |

---

## 🔧 Tech Stack

| Layer | Tool |
|---|---|
| Data Preparation | Python, Pandas, NumPy (Google Colab) |
| Visualisation | Plotly (interactive charts) |
| Dashboard | Streamlit (multi-page app) |
| AI Assistant | Groq API + LLaMA 3.3 70B |
| Deployment | Streamlit Community Cloud |

---

## 📐 Feature Engineering

Several derived features were created to improve analytical depth:

| Feature | Formula | Business Meaning |
|---|---|---|
| `CREDIT_INCOME_RATIO` | `AMT_CREDIT / AMT_INCOME_TOTAL` | How much credit relative to income |
| `ANNUITY_INCOME_RATIO` | `AMT_ANNUITY / AMT_INCOME_TOTAL` | Monthly repayment burden |
| `CREDIT_TERM` | `AMT_CREDIT / AMT_ANNUITY` | Loan repayment duration (months) |
| `AGE_YEARS` | `DAYS_BIRTH / -365` | Applicant age in years |

---

## 🔍 Key Findings

- **Maternity leave applicants** have the highest default rate at ~40%
- **Young borrowers (20–30 years)** default at 11.4%, the highest age bracket
- **Lower secondary education** holders show a 10.9% default rate
- **`EXT_SOURCE_2` and `EXT_SOURCE_3`** (external credit scores) are the strongest predictors of repayment behaviour
- Applicants with **high annuity-to-income ratios** are significantly more likely to default

---

## 🖥️ Dashboard Pages

The Streamlit app is structured into four pages:

### 1. 🏠 Executive Summary
High-level KPIs and business context — total applicants, overall default rate, top risk segments, and key takeaways for decision-makers.

### 2. 📊 Exploratory Data Analysis (EDA)
Interactive charts exploring distributions of income, credit amount, age, education, and occupation. Filters let users drill into specific segments.

### 3. 🤖 Risk Factor Analysis
Deep-dive into the variables most correlated with default — feature importance, correlation heatmaps, and segment-wise default rate comparisons.

### 4. 💬 AI Assistant
A conversational interface powered by **Groq API (LLaMA 3.3 70B)**. Users type a question and click **Ask** to get plain-English answers grounded in the dataset's findings.

**Example questions you can ask:**
- *"Which income group has the highest default rate?"*
- *"What does EXT_SOURCE_2 represent?"*
- *"How does education level affect credit risk?"*
- *"Summarise the top 3 risk factors."*

---

## 📁 Project Structure

```
credit-risk-intelligence/
│
├── data/
│   ├── raw/                  # Original Kaggle CSVs
│   └── app_final.csv         # Cleaned & merged dataset (75 cols, 307K rows)
│
├── notebooks/
│   └── data_preparation.ipynb  # Google Colab notebook for all prep work
│
├── dashboard/
│   ├── app.py                # Streamlit entry point
│   ├── pages/
│   │   ├── 1_Executive_Summary.py
│   │   ├── 2_EDA.py
│   │   ├── 3_Risk_Factor_Analysis.py
│   │   └── 4_AI_Assistant.py
│   └── utils/
│       └── helpers.py        # Shared chart/data helper functions
│
├── submission/
│   └── CreditRiskIntelligence_Report.docx  # Full assignment submission document
│
├── requirements.txt
└── README.md
```

---

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/credit-risk-intelligence.git
cd credit-risk-intelligence
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create a `.env` file or add to Streamlit secrets:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

### 4. Place the dataset
Download `app_final.csv` (the cleaned merged file) and place it in the `data/` folder.

### 5. Launch the dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📦 Requirements

```
streamlit
pandas
numpy
plotly
groq
python-dotenv
scikit-learn
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 📋 Assignment Phases Covered

This project was built as a structured data analyst assignment:

| Phase | Description |
|---|---|
| Phase 1 | Dataset selection & business problem definition |
| Phase 2 | Data preparation, cleaning & merging (5 CSVs → 1 master file) |
| Phase 3 | Exploratory Data Analysis with visual storytelling |
| Phase 4 | Interactive Streamlit dashboard (4 pages) |
| Phase 5 | AI Assistant integration (Groq + LLaMA 3.3 70B) |
| Bonus | Executive summary document with professional formatting |

---

## 💡 Business Value

This tool helps credit risk analysts and loan officers to:

- Identify high-risk applicant profiles before approval
- Understand which demographic and financial factors predict default
- Ask natural language questions about the data without needing SQL or Python skills
- Present findings to leadership through an accessible, live dashboard

---

## 👤 Author

**Kakade**
Built with ❤️ using Python, Streamlit & Groq AI

---

## 📄 License

This project is built for educational and assessment purposes using the publicly available [Home Credit Default Risk dataset](https://www.kaggle.com/competitions/home-credit-default-risk) under Kaggle's competition rules.
