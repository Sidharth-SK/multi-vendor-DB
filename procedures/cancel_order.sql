CREATE OR REPLACE PROCEDURE cancel_order(
    p_order_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_created TIMESTAMP;
BEGIN

    SELECT created_at
    INTO v_created
    FROM orders
    WHERE order_id = p_order_id;

    IF NOW() > v_created + INTERVAL '24 hours' THEN
        RAISE EXCEPTION 'Cancellation window expired';
    END IF;

    UPDATE orders
    SET order_status = 'cancelled'
    WHERE order_id = p_order_id;

END;
$$;