CREATE TABLE publishing_attempts (
    tenant_id INTEGER NOT NULL,
    attempt_id INTEGER NOT NULL,
    needs_help INTEGER CHECK (needs_help IN (0, 1)),
    PRIMARY KEY (tenant_id, attempt_id)
);

INSERT INTO publishing_attempts VALUES
    (1, 10, 1), (1, 11, NULL), (1, 12, 0), (2, 10, 1);
