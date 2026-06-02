CREATE OR REPLACE VIEW low_stock_view AS
SELECT
    p.product_name,
    w.warehouse_name,
    i.quantity_available,
    i.reorder_threshold
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
JOIN warehouses w
    ON i.warehouse_id = w.warehouse_id
WHERE i.quantity_available <
      i.reorder_threshold;