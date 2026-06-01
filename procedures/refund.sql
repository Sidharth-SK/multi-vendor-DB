CREATE OR REPLACE PROCEDURE refund_payment(
    p_payment_id INT,
    p_refund_amount NUMERIC(10,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_amount NUMERIC(10,2);
BEGIN

    SELECT amount
    INTO v_amount
    FROM payments
    WHERE payment_id = p_payment_id;

    IF p_refund_amount > v_amount THEN
        RAISE EXCEPTION
        'Refund exceeds payment amount';
    END IF;

    INSERT INTO refunds(
        payment_id,
        refund_amount,
        refund_method,
        processed_at
    )
    VALUES(
        p_payment_id,
        p_refund_amount,
        'original',
        NOW()
    );

    UPDATE payments
    SET payment_status = 'refunded'
    WHERE payment_id = p_payment_id;

END;
$$;