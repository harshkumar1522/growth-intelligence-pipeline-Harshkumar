# growth-intelligence-pipeline-Harshkumar

A connected, end-to-end retail analytics pipeline built as a capstone project for the E&ICT Academy IIT Roorkee.

The project analyzes retail growth, revenue, customer behavior, product performance, and returns using a three-layer pipeline:

**SQL → Python → GenAI Narrator**

The central business question is:

> **Are product returns eating into revenue and growth, and what should regional operations and finance teams pay attention to?**

---

## Project Objective

The goal of this project is to build a reproducible analytics pipeline where each layer depends on the output of the previous layer.

The pipeline is designed around three stages:

1. **SQL Analytics**
   - Load and query raw retail data
   - Calculate revenue, order metrics, customer rankings, category performance, and return rates
   - Validate data quality through SQL

2. **Python Analytics**
   - Clean and standardize the raw data
   - Remove duplicate transactions
   - Handle missing values
   - Detect quantity outliers
   - Perform segmentation, correlation analysis, and monthly revenue analysis
   - Generate visualizations

3. **GenAI Narrator**
   - Consume verified findings from the Python layer
   - Generate a management-friendly narrative
   - Prevent the AI from inventing or modifying numerical findings
   - Provide an offline fallback when an API key or network connection is unavailable

---

## Important Data Integrity Rule

Each layer must only report numbers that it either:

- computed itself, or
- received from the immediately preceding layer.

No layer is allowed to invent, manually modify, or independently recreate figures that belong to another layer.

The raw CSV files are preserved exactly as supplied.

All data cleaning is performed programmatically in Python.

---

## Repository Structure

```text
Growth-Intelligence-Pipeline/
│
├── README.md
├── requirements.txt
│
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
│
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
│
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
│
└── narrator/
    ├── findings.json
    ├── generate_narrative.py
    └── sample_output.txt
