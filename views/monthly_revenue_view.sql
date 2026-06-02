CREATE OR REPLACE VIEW monthly_revenue_view AS
WITH monthly_sales AS
(
    SELECT
        p.seller_id,
        DATE_TRUNC('month', o.created_at) AS sales_month,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    GROUP BY
        p.seller_id,
        DATE_TRUNC('month', o.created_at)
)
SELECT
    seller_id,
    sales_month,
    revenue,
    ROUND(
        (
            revenue -
            LAG(revenue) OVER (
                PARTITION BY seller_id
                ORDER BY sales_month
            )
        ) * 100.0 /
        NULLIF(
            LAG(revenue) OVER (
                PARTITION BY seller_id
                ORDER BY sales_month
            ),
            0
        ),
        2
    ) AS growth_pct
FROM monthly_sales;