-- Active: 1780247294100@@127.0.0.1@5432@multi_vendor_db@public
SELECT
    c.category_id,
    p.product_id,
    p.product_name,
    SUM(oi.quantity * oi.unit_price) AS revenue,
    RANK() OVER(
        PARTITION BY c.category_id
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC
    ) rank_no
FROM products p
JOIN product_categories pc
    ON p.product_id = pc.product_id
JOIN categories c
    ON pc.category_id = c.category_id
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY c.category_id,
         p.product_id,
         p.product_name;

WITH ranked_products AS
(
    SELECT
        c.category_id,
        p.product_id,
        p.product_name,
        SUM(oi.quantity) AS total_sold,
        RANK() OVER(
            PARTITION BY c.category_id
            ORDER BY SUM(oi.quantity) DESC
        ) rnk
    FROM products p
    JOIN product_categories pc
        ON p.product_id = pc.product_id
    JOIN categories c
        ON pc.category_id = c.category_id
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY c.category_id,
             p.product_id,
             p.product_name
)
SELECT *
FROM ranked_products
WHERE rnk <= 5;

SELECT
    customer_id,
    order_id,
    created_at,
    ROW_NUMBER() OVER(
        PARTITION BY customer_id
        ORDER BY created_at
    ) AS purchase_number
FROM orders;

WITH monthly_sales AS
(
    SELECT
        p.seller_id,
        DATE_TRUNC('month', o.created_at) AS month,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY p.seller_id,
             DATE_TRUNC('month', o.created_at)
)
SELECT
    *,
    SUM(revenue) OVER(
        PARTITION BY seller_id
        ORDER BY month
    ) AS running_revenue
FROM monthly_sales;

