CREATE OR REPLACE PROCEDURE place_order(
    p_customer_id INT,
    p_cart_id INT,
    p_payment_method VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC(10,2);
    v_order_id INT;
    rec RECORD;
BEGIN

    BEGIN

        -- Lock inventory rows
        FOR rec IN
        SELECT ci.product_id,
               ci.quantity,
               i.inventory_id,
               i.quantity_available
        FROM cart_items ci
        JOIN inventory i
            ON ci.product_id = i.product_id
        WHERE ci.cart_id = p_cart_id
        FOR UPDATE
        LOOP

            IF rec.quantity_available < rec.quantity THEN
                RAISE EXCEPTION
                'Insufficient stock for product %',
                rec.product_id;
            END IF;

        END LOOP;

        SELECT SUM(p.base_price * ci.quantity)
        INTO v_total
        FROM cart_items ci
        JOIN products p
            ON ci.product_id = p.product_id
        WHERE ci.cart_id = p_cart_id;

        INSERT INTO orders(
            customer_id,
            order_status,
            total_amount,
            created_at
        )
        VALUES(
            p_customer_id,
            'pending',
            v_total,
            NOW()
        )
        RETURNING order_id INTO v_order_id;

        INSERT INTO order_items(
            order_id,
            product_id,
            quantity,
            unit_price
        )
        SELECT
            v_order_id,
            p.product_id,
            ci.quantity,
            p.base_price
        FROM cart_items ci
        JOIN products p
            ON ci.product_id = p.product_id
        WHERE ci.cart_id = p_cart_id;

        INSERT INTO payments(
            order_id,
            payment_method,
            payment_status,
            amount
        )
        VALUES(
            v_order_id,
            p_payment_method,
            'success',
            v_total
        );

        COMMIT;

    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END;

END;
$$;