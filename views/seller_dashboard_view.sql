CREATE OR REPLACE VIEW seller_dashboard_view AS
WITH seller_metrics AS
(
    SELECT
        p.seller_id,

        SUM(
            oi.quantity * oi.unit_price
        ) revenue,

        COUNT(
            DISTINCT oi.order_id
        ) order_count,

        AVG(rt.rating_value)
            avg_rating
    FROM products p
    LEFT JOIN order_items oi
        ON p.product_id = oi.product_id
    LEFT JOIN ratings rt
        ON p.product_id = rt.product_id
    GROUP BY p.seller_id
)
SELECT *
FROM seller_metrics;

