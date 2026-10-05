-- Task 3(a) — Order totals
-- Exact output:
-- total_orders | total_revenue | avg_order_value
-- 180 | 99860.20 | 554.78

SELECT
    COUNT(*) AS total_orders,
    ROUND(
        SUM(
            quantity * price *
            (1 - COALESCE(discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_revenue,
    ROUND(
        AVG(
            quantity * price *
            (1 - COALESCE(discount_pct, 0) / 100.0)
        ),
        2
    ) AS avg_order_value
FROM orders
JOIN products
    ON orders.product_id = products.product_id;


-- Task 3(b) — COUNT(*) vs COUNT(rating)
-- Exact output:
-- total_rows | rated_orders | unrated_orders
-- 180 | 165 | 15

SELECT
    COUNT(*) AS total_rows,
    COUNT(rating) AS rated_orders,
    COUNT(*) - COUNT(rating) AS unrated_orders
FROM orders;

-- ============================================================
-- Task 3(c): Customers with zero orders
-- Expected output:
-- C045 | Vihaan
-- ============================================================

-- Method 1: LEFT JOIN + HAVING
SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = 0;

-- Method 2: Independent NOT IN check
SELECT
    c.customer_id,
    c.name
FROM customers c
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
);


-- ============================================================
-- Task 3(d): Cities with return rate above 20%
-- Expected output:
-- Jaipur    | 19 | 8 | 42.1
-- Lucknow   | 49 | 15 | 30.6
-- Bangalore | 33 | 8 | 24.2
-- ============================================================

SELECT
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(
        100.0 * SUM(o.returned) / COUNT(o.order_id),
        1
    ) AS return_rate_pct
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;


-- ============================================================
-- Task 3(e): Customer ranking by total spend
-- Tie-break rule: customer_id ASC is used when two customers
-- have the same total spend, ensuring deterministic ranking.
--
-- Expected Top 5:
-- C043 | Reyansh | 12920.00
-- C026 | Isha    | 8371.60
-- C008 | Meera   | 4564.60
-- C011 | Arjun   | 4111.00
-- C042 | Sanya   | 3785.00
-- ============================================================

-- Top 5 customers
SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;

-- LIMIT 3 OFFSET 2
SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;


-- ============================================================
-- Task 3(f): Category order count and revenue
--
-- Expected output:
-- Haircare     | 54 | 44956.10
-- Skincare     | 60 | 27346.00
-- Babycare     | 30 | 16805.00
-- PersonalCare | 36 | 10753.10
-- ============================================================

SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS category_revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;


-- ============================================================
-- Task 3(g): Customers whose name starts with A
--
-- Expected output: 10 customers
-- ============================================================

SELECT
    customer_id,
    name
FROM customers
WHERE name LIKE 'A%'
ORDER BY customer_id;


-- ============================================================
-- Task 3(g): Customers whose name starts with A
--
-- Expected output: 10 customers
-- ============================================================

SELECT
    customer_id,
    name
FROM customers
WHERE name LIKE 'A%'
ORDER BY customer_id;


-- ============================================================
-- Task 3(h): Distinct customer acquisition sources
--
-- Expected output:
-- Ad
-- Organic
-- Referral
-- Social
-- ============================================================

SELECT DISTINCT
    acquisition_source
FROM customers
ORDER BY acquisition_source;


-- ============================================================
-- Task 3(i): Add and populate loyalty tier
-- Gold = city_tier 1
-- Silver = city_tier 2
--
-- Expected output:
-- Gold   | 28
-- Silver | 17
-- ============================================================

ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;

SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier
ORDER BY loyalty_tier DESC;

