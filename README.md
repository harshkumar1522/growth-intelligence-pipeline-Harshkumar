# Growth Intelligence Pipeline

A connected 3-layer data analytics and GenAI pipeline built for a Mamaearth-style retail growth analytics scenario.

The project analyzes customer, product, and order data to understand revenue performance, returns, data-quality issues, high-risk customer segments, and monthly revenue trends. The final layer converts verified analytical findings into a business narrative using Gemini with a fully deterministic offline fallback.

---

## Project Objective

The objective of this project is to build a reliable analytics pipeline that answers key business questions around:

- Revenue performance
- Customer and product behavior
- Return rates
- Payment-method risk
- City-tier risk
- Data-quality issues
- Quantity outliers
- Monthly revenue trends
- Revenue reconciliation
- AI-powered business interpretation

The pipeline is designed for regional operations and finance teams who need trustworthy, reproducible insights.

---

## Pipeline Architecture

The project contains three connected layers:

```text
Raw CSV Data
     │
     ▼
┌─────────────────────┐
│     PART 1 - SQL    │
│                     │
│ Schema + Seed Data  │
│ Business Reports    │
└─────────┬───────────┘
          │
          │ Verified SQL figures
          ▼
┌─────────────────────┐
│   PART 2 - PYTHON   │
│                     │
│ Cleaning + EDA      │
│ Reconciliation      │
│ Outlier Analysis    │
│ Segmentation        │
│ Correlation         │
│ Visualizations      │
└─────────┬───────────┘
          │
          │ Verified findings
          ▼
┌─────────────────────┐
│  PART 3 - GENAI     │
│                     │
│ findings.json       │
│ Gemini Narrator     │
│ SCR Narrative       │
│ Offline Fallback    │
└─────────────────────┘
