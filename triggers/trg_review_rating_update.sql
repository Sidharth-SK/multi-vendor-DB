ALTER TABLE products
ADD COLUMN average_rating NUMERIC(3,2);

CREATE OR REPLACE FUNCTION update_product_rating()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    UPDATE products
    SET average_rating =
    (
        SELECT AVG(rating_value)
        FROM ratings
        WHERE product_id = NEW.product_id
    )
    WHERE product_id = NEW.product_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_review_rating_update
AFTER INSERT ON ratings
FOR EACH ROW
EXECUTE FUNCTION update_product_rating();