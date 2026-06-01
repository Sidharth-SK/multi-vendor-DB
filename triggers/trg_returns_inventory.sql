CREATE OR REPLACE FUNCTION restore_inventory()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    UPDATE inventory
    SET quantity_available =
        quantity_available + 1
    WHERE product_id =
    (
        SELECT product_id
        FROM order_items
        WHERE order_item_id = NEW.order_item_id
    );

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_returns_inventory
AFTER INSERT ON returns
FOR EACH ROW
EXECUTE FUNCTION restore_inventory();