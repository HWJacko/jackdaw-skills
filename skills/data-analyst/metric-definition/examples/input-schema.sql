CREATE TABLE main.publishing_attempts (
    tenant_id INTEGER NOT NULL,
    attempt_id INTEGER NOT NULL,
    started_at TEXT NOT NULL,
    needs_help INTEGER CHECK (needs_help IN (0, 1)),
    PRIMARY KEY (tenant_id, attempt_id)
);

CREATE TABLE main.attempt_notes (
    tenant_id INTEGER NOT NULL,
    attempt_id INTEGER NOT NULL,
    note_id INTEGER NOT NULL,
    PRIMARY KEY (tenant_id, attempt_id, note_id),
    FOREIGN KEY (tenant_id, attempt_id)
        REFERENCES publishing_attempts (tenant_id, attempt_id)
);
