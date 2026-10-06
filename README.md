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

```text
Raw CSV Data
     |
     v
+---------------------+
|     PART 1 - SQL    |
|                     |
| Schema + Seed Data  |
| Business Reports    |
+----------+----------+
           |
           | Verified SQL figures
           v
+---------------------+
|   PART 2 - PYTHON   |
|                     |
| Cleaning + EDA      |
| Reconciliation      |
| Outlier Analysis    |
| Segmentation        |
| Correlation         |
| Visualizations      |
+----------+----------+
           |
           | Verified findings
           v
+---------------------+
|  PART 3 - GENAI     |
|                     |
| findings.json       |
| Gemini Narrator     |
| SCR Narrative       |
| Offline Fallback    |
+---------------------+


## Data Integrity Principle

No layer reports a number that it did not compute itself or receive from the preceding layer.

The raw CSV files are preserved exactly as supplied. Data cleaning is performed programmatically in Python rather than by manually editing the source files.

Repository Structure

growth-intelligence-pipeline-Harshkumar/
|
|-- README.md
|-- requirements.txt
|
|-- data/
|   |-- customers.csv
|   |-- products.csv
|   `-- orders.csv
|
|-- sql/
|   |-- schema.sql
|   |-- seed_data.sql
|   `-- reports.sql
|
|-- analysis/
|   |-- clean_and_eda.py
|   `-- visualize.py
|
|-- visualizations/
|   |-- return_rate_by_payment.png
|   `-- monthly_revenue_trend.png
|
`-- narrator/
    |-- findings.json
    |-- generate_narrative.py
    `-- sample_output.txt
Dataset

The project uses three CSV files.

customers.csv

Contains customer-level information:

Customer ID
Name
City
City Tier
Signup Date
Acquisition Source

Total customers:

45
products.csv

Contains product information:

Product ID
Product Name
Category
Price

Total products:

16
orders.csv

Contains transaction-level information:

Order ID
Customer ID
Product ID
Order Date
Quantity
Discount
Payment Method
Rating
Returned Flag

Raw order count:

180

The raw dataset intentionally contains several data-quality issues that are handled programmatically in Part 2.

Part 1 — SQL Analytics
Files
sql/schema.sql
sql/seed_data.sql
sql/reports.sql
Schema

schema.sql creates the following tables:

customers
products
orders

Primary keys and foreign-key relationships are defined between the tables.

Seed Data

seed_data.sql loads the supplied CSV data into the database.

The seed script is re-runnable and clears the existing tables before inserting the data.

Expected row counts after loading:

customers = 45
products  = 16
orders    = 180
SQL Reports

reports.sql contains the required business analysis queries covering:

Total orders
Total revenue
Average order value
Returned orders
Non-returned orders
Customer identification using joins
City-level return analysis
Top customers
Category-level revenue
Customer name filtering
Acquisition-source analysis
Customer loyalty-tier analysis
Part 2 — Python Data Cleaning and EDA
Files
analysis/clean_and_eda.py
analysis/visualize.py

The Python layer uses Pandas and NumPy to clean, reconcile, analyze and visualize the raw data.

Task 1 — Data Loading and Inspection

All three CSV files are loaded using Pandas.

The raw orders dataset has:

180 rows x 9 columns
Task 2 — Payment Method Standardization

Payment-method casing is standardized using uppercase formatting.

Raw dataset:

7 unique payment-method values

After standardization:

CARD = 70
UPI  = 55
COD  = 55

Final unique payment methods:

3
Task 3 — Duplicate Detection

Duplicate transactions are identified using the natural transaction key rather than order_id.

Five duplicate transaction rows are detected:

O0176
O0177
O0178
O0179
O0180

After removing these duplicates:

180 -> 175 rows

The raw CSV remains unchanged.

Task 4 — Missing-Value Treatment

Missing discounts are imputed as:

0%

Missing ratings are imputed using the median rating:

3.0

After imputation, there are no missing values in the cleaned analytical dataset.

Task 5 — Revenue Reconciliation

Revenue is calculated in Python using:

quantity x price x (1 - discount_pct / 100)

Cleaned Python revenue:

₹97,358.30

Raw SQL revenue:

₹99,860.20

Difference:

₹2,501.90

The reconciliation difference is attributable to the five duplicate transactions removed during Python cleaning.

Task 6 — Quantity Outlier Detection

The IQR method is used to identify unusual order quantities.

Results:

Q1  = 1.0
Q3  = 2.0
IQR = 1.0

Outlier boundaries:

Lower bound = -0.5
Upper bound = 3.5

Two quantity outliers are identified:

O0011 = quantity 25
O0098 = quantity 30

These records are flagged rather than deleted.

Task 7 — COD Return Hypothesis

Return rates by payment method:

CARD = 14.7%
COD  = 44.4%
UPI  = 18.9%

The analysis confirms that COD has the highest return rate.

Conclusion:

COD return hypothesis = Confirmed
Task 8 — Multi-Level Risk Segmentation

Return rates are segmented using:

payment_method x city_tier

The highest-risk segment is:

COD + City Tier 2
Return Rate = 54.5%

For comparison:

COD + City Tier 1 = 37.5%

This identifies COD orders from Tier-2 cities as the highest-risk operational segment.

Task 9 — Correlation Analysis

The correlation matrix includes:

rating
returned
discount_pct
quantity

All six pairwise relationships are negligible.

The discount-versus-return correlation is approximately:

-0.09

Therefore, the data does not show a meaningful relationship between higher discounts and lower returns.

Task 10 — Monthly Revenue and Outlier Correction

Monthly revenue after quantity-outlier correction:

Month	Revenue
2026-01	₹11,637.10
2026-02	₹13,195.50
2026-03	₹20,318.90
2026-04	₹9,495.30
2026-05	₹13,151.10
2026-06	₹11,615.40

The apparent peak before outlier correction was:

January 2026 = ₹29,582.10

After correcting the flagged quantity outliers:

January 2026 = ₹11,637.10

The true revenue peak is therefore:

March 2026 = ₹20,318.90
Visualizations

The project generates two required visualizations.

Return Rate by Payment Method
visualizations/return_rate_by_payment.png

This visualization highlights the substantially higher return rate associated with COD.

Monthly Revenue Trend
visualizations/monthly_revenue_trend.png

This visualization shows the corrected monthly revenue trend after excluding flagged quantity outliers.

Part 3 — GenAI-Powered Insight Narrator
Files
narrator/findings.json
narrator/generate_narrative.py
narrator/sample_output.txt

The GenAI layer converts verified Part 1 and Part 2 findings into a concise business narrative.

findings.json

findings.json contains the verified figures passed from the analytical layer to the narrator.

Key findings include:

Cleaned revenue       = ₹97,358.30
Raw SQL revenue       = ₹99,860.20
Reconciliation delta  = ₹2,501.90

CARD return rate      = 14.7%
COD return rate       = 44.4%
UPI return rate       = 18.9%

Highest-risk segment  = COD + Tier 2
Highest-risk rate     = 54.5%

True peak month       = 2026-03
True peak revenue     = ₹20,318.90

Inflated month        = 2026-01
Apparent revenue      = ₹29,582.10
Corrected revenue     = ₹11,637.10

The findings file is generated from verified analytical results rather than manually changing the raw data.

Gemini Narrator

generate_narrative.py uses the Google GenAI client library.

The narrator follows the Situation-Complication-Resolution structure:

Situation
Complication
Resolution

The system instruction fixes the agent's role as a senior data analyst writing for Mamaearth's regional operations and finance heads.

The model is instructed that every number in the output must come only from the supplied findings.

This prevents the model from inventing additional statistics.

Gemini API Configuration

The Gemini API key is never stored directly inside the Python source code.

Set the API key as an environment variable:

GEMINI_API_KEY

In Google Colab, the key can be stored using Colab Secrets.

Example:

from google.colab import userdata
import os

os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")

Never commit the API key to GitHub.

Offline Fallback

The pipeline includes a fully deterministic offline fallback.

If:

no Gemini API key is configured, or
the Gemini API request fails,

the pipeline can generate an offline S-C-R narrative using only the verified values in findings.json.

The offline path requires:

No API key
No network access
No paid API usage

This ensures the project remains reproducible and gradable even when the Gemini API is unavailable.

Numeric Accuracy Check

The narrator output is checked for the required verified figures.

The required values are:

97,358.30
44.4
54.5
2,501.90
20,318.90

The true peak month must also correspond to:

March 2026

The checker normalizes commas and verifies that the required values are present in the saved narrative.

Reproducibility — Complete Execution Order

A new user should be able to reproduce the entire project in the following order.

Step 1 — Load the SQL Schema

Create a SQLite database and execute:

sql/schema.sql
Step 2 — Load the Seed Data

Execute:

sql/seed_data.sql

Expected row counts:

Customers = 45
Products  = 16
Orders    = 180
Step 3 — Run SQL Reports

Execute:

sql/reports.sql

This produces the required Part 1 business analysis.

Step 4 — Run Python Cleaning and EDA

Run:

python analysis/clean_and_eda.py

This performs:

CSV loading
Data inspection
Payment-method standardization
Duplicate detection
Missing-value treatment
Data merging
Revenue calculation
Revenue reconciliation
IQR outlier detection
Return-rate analysis
Risk segmentation
Correlation analysis
Monthly revenue analysis
Step 5 — Generate Visualizations

Run:

python analysis/visualize.py

This generates:

visualizations/return_rate_by_payment.png
visualizations/monthly_revenue_trend.png
Step 6 — Generate Findings

The verified analytical results are exported into:

narrator/findings.json

The findings file becomes the controlled input for the GenAI narrator.

Step 7 — Run the GenAI Narrator

Set:

GEMINI_API_KEY

as an environment variable and run the narrator.

The online path attempts Gemini generation.

If the API is unavailable, the offline deterministic fallback can be used.

Step 8 — Save the Sample Narrative

The final verified narrative is stored in:

narrator/sample_output.txt

This file is the saved sample used for numeric validation.

Business Findings
1. Returns are strongly associated with COD

COD has a return rate of:

44.4%

compared with:

CARD = 14.7%
UPI  = 18.9%

COD therefore represents the clearest return-risk area in the dataset.

2. Tier-2 COD orders are the highest-risk segment

The highest-risk segment is:

COD + Tier 2
54.5% return rate

This segment should receive particular attention from regional operations.

3. Revenue reconciliation identifies duplicate transactions

The difference between SQL revenue and cleaned Python revenue is:

₹2,501.90

This difference is attributable to five duplicate transactions.

4. January revenue was artificially inflated

January initially appeared to be the highest-revenue month because of two bulk quantity outliers.

After correcting the outliers:

March 2026 = ₹20,318.90

becomes the true revenue peak.

5. Discounts do not show a meaningful return relationship

The discount-return correlation is approximately:

-0.09

indicating a negligible relationship in this dataset.

Technology Stack
Python
Pandas
NumPy
Matplotlib
SQLite
SQL
Google Colab
Google Gemini API
Google GenAI Python SDK
GitHub
Requirements

Install the Python dependencies using:

pip install -r requirements.txt

The project requires:

pandas
numpy
matplotlib
google-genai
Data Integrity and Security


The following practices are followed:

Raw CSV files are preserved unchanged.
Cleaning is performed programmatically.
Duplicate transactions are identified using a natural transaction key.
API keys are stored as environment variables or Colab Secrets.
API keys are never committed to GitHub.
Verified findings are passed from the analytical layer to the GenAI layer.
The GenAI narrator is constrained to use supplied findings rather than inventing statistics.
A deterministic offline fallback is provided for zero-network execution.
Final Verified Metrics
Raw orders                         180
Cleaned orders                     175

Raw SQL revenue              ₹99,860.20
Cleaned Python revenue        ₹97,358.30
Reconciliation delta           ₹2,501.90

CARD return rate                   14.7%
COD return rate                    44.4%
UPI return rate                    18.9%

Highest-risk segment       COD + Tier 2
Highest-risk return rate             54.5%

January apparent revenue     ₹29,582.10
January corrected revenue     ₹11,637.10

True peak month                  March 2026
True peak revenue             ₹20,318.90

Conclusion

The Growth Intelligence Pipeline demonstrates a complete analytics workflow from raw transactional data to SQL reporting, Python-based data cleaning and exploratory analysis, visual analytics, and a GenAI-powered business narrative.

The pipeline emphasizes:

Reproducibility
Numerical accuracy
Data-quality handling
Transparent revenue reconciliation
Reliable business analytics
Safe AI integration
Deterministic offline fallback
