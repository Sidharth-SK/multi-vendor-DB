CREATE OR REPLACE VIEW abandoned_cart_view AS
SELECT
    c.cart_id,
    u.email,

    COUNT(ci.cart_item_id)
        item_count,

    SUM(
        ci.quantity *
        p.base_price
    ) total_value,

    EXTRACT(
        DAY FROM (
            NOW() - c.expires_at
        )
    ) age_days

FROM cart c
JOIN users u
    ON c.customer_id = u.user_id
JOIN cart_items ci
    ON c.cart_id = ci.cart_id
JOIN products p
    ON ci.product_id = p.product_id

WHERE c.expires_at < NOW()

GROUP BY
    c.cart_id,
    u.email,
    c.expires_at;