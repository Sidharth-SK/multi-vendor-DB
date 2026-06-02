CREATE OR REPLACE VIEW customer_order_history_view AS
SELECT
    u.full_name,
    o.order_id,
    o.order_status,
    p.payment_status,
    CASE
        WHEN r.return_id IS NOT NULL THEN 'Returned'
        ELSE 'Not Returned'
    END AS return_status
FROM orders o
JOIN users u
    ON o.customer_id = u.user_id
LEFT JOIN payments p
    ON o.order_id = p.order_id
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN returns r
    ON oi.order_item_id = r.order_item_id;