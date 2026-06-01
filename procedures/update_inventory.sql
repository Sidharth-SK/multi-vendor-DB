CREATE OR REPLACE PROCEDURE update_inventory(
    p_inventory_id INT,
    p_change INT,
    p_movement_type VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_qty INT;
    v_product INT;
    v_warehouse INT;
BEGIN

    SELECT quantity_available,
           product_id,
           warehouse_id
    INTO v_qty,
         v_product,
         v_warehouse
    FROM inventory
    WHERE inventory_id = p_inventory_id;

    IF v_qty + p_change < 0 THEN
        RAISE EXCEPTION 'Negative inventory not allowed';
    END IF;

    UPDATE inventory
    SET quantity_available =
        quantity_available + p_change
    WHERE inventory_id = p_inventory_id;

    INSERT INTO stock_movements(
        product_id,
        warehouse_id,
        movement_type,
        quantity,
        movement_date
    )
    VALUES(
        v_product,
        v_warehouse,
        p_movement_type,
        ABS(p_change),
        NOW()
    );

END;
$$;