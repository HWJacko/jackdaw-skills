CREATE TABLE main.orders (
    tenant_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    PRIMARY KEY (tenant_id, order_id)
);
