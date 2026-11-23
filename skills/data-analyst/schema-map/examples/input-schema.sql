CREATE TABLE main.customers (
    tenant_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    display_name TEXT NOT NULL,
    PRIMARY KEY (tenant_id, customer_id)
);

CREATE TABLE main.orders (
    tenant_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    total_minor INTEGER NOT NULL,
    currency_code TEXT NOT NULL,
    PRIMARY KEY (tenant_id, order_id)
);

CREATE TABLE main.order_items (
    tenant_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    PRIMARY KEY (tenant_id, order_id, line_number),
    FOREIGN KEY (tenant_id, order_id)
        REFERENCES orders (tenant_id, order_id)
);
