CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_inventory_product
ON inventory(product_id);

CREATE INDEX idx_inventory_warehouse
ON inventory(warehouse_id);

CREATE INDEX idx_products_seller
ON products(seller_id);

CREATE INDEX idx_products_brand
ON products(brand_id);