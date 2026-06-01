CREATE OR REPLACE FUNCTION deduct_inventory()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    UPDATE inventory
    SET quantity_available =
        quantity_available - NEW.quantity
    WHERE product_id = NEW.product_id;

    INSERT INTO stock_movements(
        product_id,
        warehouse_id,
        movement_type,
        quantity,
        movement_date
    )
    SELECT
        product_id,
        warehouse_id,
        'stock_out',
        NEW.quantity,
        NOW()
    FROM inventory
    WHERE product_id = NEW.product_id
    LIMIT 1;

    RETURN NEW;
END;
$$;


CREATE TRIGGER trg_order_items_inventory
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION deduct_inventory();