-- Active: 1780247294100@@127.0.0.1@5432@multi_vendor_db@public
SELECT
    p.product_id,
    p.product_name,
    sp.business_name AS seller_name,
    b.brand_name,
    c.category_name
FROM products p
INNER JOIN seller_profiles sp
    ON p.seller_id = sp.seller_id
INNER JOIN brands b
    ON p.brand_id = b.brand_id
INNER JOIN product_categories pc
    ON p.product_id = pc.product_id
INNER JOIN categories c
    ON pc.category_id = c.category_id;

SELECT
    cp.customer_id,
    u.full_name,
    u.email
FROM customer_profiles cp
INNER JOIN users u
    ON cp.customer_id = u.user_id
LEFT JOIN orders o
    ON cp.customer_id = o.customer_id
WHERE o.order_id IS NULL;

SELECT
    sp.seller_id,
    sp.business_name,
    COUNT(p.product_id) AS total_products
FROM seller_profiles sp
LEFT JOIN products p
    ON sp.seller_id = p.seller_id
GROUP BY sp.seller_id, sp.business_name
ORDER BY total_products DESC;

SELECT DISTINCT
    o.order_id,
    uc.full_name AS customer_name,
    us.full_name AS seller_name,
    o.total_amount
FROM orders o
INNER JOIN users uc
    ON o.customer_id = uc.user_id
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
INNER JOIN products p
    ON oi.product_id = p.product_id
INNER JOIN seller_profiles sp
    ON p.seller_id = sp.seller_id
INNER JOIN users us
    ON sp.seller_id = us.user_id;

SELECT *
FROM products p
WHERE EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.product_id = p.product_id
);

SELECT *
FROM products p
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items oi
    WHERE oi.product_id = p.product_id
);

SELECT
    p.product_id,
    p.product_name,
    p.base_price,
    c.category_name
FROM products p
JOIN product_categories pc
    ON p.product_id = pc.product_id
JOIN categories c
    ON pc.category_id = c.category_id
WHERE p.base_price >
(
    SELECT AVG(p2.base_price)
    FROM products p2
    JOIN product_categories pc2
        ON p2.product_id = pc2.product_id
    WHERE pc2.category_id = pc.category_id
);

SELECT *
FROM
(
    SELECT
        p.*,
        ROW_NUMBER() OVER(
            PARTITION BY seller_id
            ORDER BY base_price DESC
        ) rn
    FROM products p
) x
WHERE rn <= 3;


SELECT
    customer_id
FROM orders
WHERE created_at >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY customer_id
HAVING COUNT(
        DISTINCT DATE_TRUNC('month', created_at)
      ) = 6;

SELECT
    c.*
FROM coupons c
LEFT JOIN coupon_usage cu
    ON c.coupon_id = cu.coupon_id
WHERE cu.usage_id IS NULL;

WITH seller_sales AS
(
    SELECT
        p.seller_id,
        p.product_id,
        p.product_name,
        SUM(oi.quantity) AS qty_sold,
        ROW_NUMBER() OVER(
            PARTITION BY p.seller_id
            ORDER BY SUM(oi.quantity) DESC
        ) rn
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.seller_id, p.product_id, p.product_name
)
SELECT *
FROM seller_sales
WHERE rn = 1;

SELECT
    o.order_id,
    p.payment_id,
    pt.transaction_id,
    pt.transaction_status
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
JOIN payment_transactions pt
    ON p.payment_id = pt.payment_id
WHERE LOWER(pt.transaction_status) = 'failed';

SELECT
    p.product_id,
    p.product_name,
    ROUND(AVG(rt.rating_value),2) AS avg_rating,
    COUNT(DISTINCT rv.review_id) AS review_count
FROM products p
LEFT JOIN ratings rt
    ON p.product_id = rt.product_id
LEFT JOIN reviews rv
    ON p.product_id = rv.product_id
GROUP BY p.product_id, p.product_name;

WITH seller_revenue AS
(
    SELECT
        p.seller_id,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.seller_id
)
SELECT *
FROM seller_revenue
WHERE revenue >
(
    SELECT AVG(revenue)
    FROM seller_revenue
);

WITH repeat_customers AS
(
    SELECT
        customer_id,
        COUNT(*) AS completed_orders
    FROM orders
    WHERE order_status = 'delivered'
    GROUP BY customer_id
)
SELECT *
FROM repeat_customers
WHERE completed_orders > 5;

WITH RECURSIVE category_tree AS
(
    SELECT
        category_id,
        category_name,
        parent_category_id,
        category_name::TEXT AS path
    FROM categories
    WHERE parent_category_id IS NULL

    UNION ALL

    SELECT
        c.category_id,
        c.category_name,
        c.parent_category_id,
        ct.path || ' -> ' || c.category_name
    FROM categories c
    JOIN category_tree ct
        ON c.parent_category_id = ct.category_id
)
SELECT *
FROM category_tree
ORDER BY path;