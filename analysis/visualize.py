
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# PART 2 — VISUALIZATIONS
# ============================================================

# Load raw data
orders = pd.read_csv("/content/data/orders.csv")
customers = pd.read_csv("/content/data/customers.csv")
products = pd.read_csv("/content/data/products.csv")

# Standardize payment method
orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

# Remove duplicate transactions
duplicate_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

duplicate_mask = orders.duplicated(
    subset=duplicate_key,
    keep="first"
)

orders_clean = orders.loc[~duplicate_mask].copy()

# Impute missing values
orders_clean["discount_pct"] = orders_clean["discount_pct"].fillna(0)
orders_clean["rating"] = orders_clean["rating"].fillna(
    orders_clean["rating"].median()
)

# Merge with products
merged = orders_clean.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Calculate order value
merged["order_value"] = (
    merged["quantity"]
    * merged["price"]
    * (1 - merged["discount_pct"] / 100)
)

# ============================================================
# Visualization 1: Return rate by payment method
# ============================================================

return_rates = (
    merged.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .reindex(["CARD", "COD", "UPI"])
)

plt.figure(figsize=(8, 5))
return_rates.plot(kind="bar")

plt.title("Return Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "/content/visualizations/return_rate_by_payment.png",
    dpi=150
)

plt.close()

# ============================================================
# Visualization 2: Outlier-corrected monthly revenue
# ============================================================

merged["order_date"] = pd.to_datetime(merged["order_date"])

Q1 = merged["quantity"].quantile(0.25)
Q3 = merged["quantity"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

merged["is_outlier"] = (
    (merged["quantity"] < lower_bound) |
    (merged["quantity"] > upper_bound)
)

corrected = merged[~merged["is_outlier"]].copy()

corrected["year_month"] = (
    corrected["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_revenue = (
    corrected
    .groupby("year_month")["order_value"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(9, 5))
monthly_revenue.plot(marker="o")

plt.title("Monthly Revenue Trend — Outlier Corrected")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "/content/visualizations/monthly_revenue_trend.png",
    dpi=150
)

plt.close()

print("✅ Both visualizations generated successfully.")
print("\nFiles created:")

for filename in [
    "return_rate_by_payment.png",
    "monthly_revenue_trend.png"
]:
    path = f"/content/visualizations/{filename}"
    print(
        filename,
        "→",
        "EXISTS" if os.path.exists(path) else "MISSING"
    )
