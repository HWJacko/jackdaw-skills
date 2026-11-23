# Read-only Schema Inspection

Use the database tool already available to the agent. This skill does not supply a database connection.
Confirm the dialect and scope from connection metadata or supplied context before choosing catalogue queries.
Use the installed database version's documentation when its metadata differs from these examples.

## Inspection order

1. List included schemas, tables, and views. Record the current identity's visibility limits.
2. Read columns, types, null rules, defaults, generated fields, and comments.
3. Read primary and unique keys. Keep composite column order.
4. Read foreign keys. Pair source and target columns by constraint and position.
5. Read view definitions and constraint enforcement where permitted. Record missing access.

Keep the catalogue query and its scope as an evidence reference. Do not copy connection strings.
Do not infer a missing constraint from an empty result if the metadata view can hide it.
Do not claim that declarations validate current data or establish business meanings.

## PostgreSQL

Use `information_schema.tables` and `information_schema.columns` for the visible object inventory.
The following queries read metadata only. Apply an approved schema filter when scope is narrower.

```sql
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
```

```sql
SELECT table_schema, table_name, column_name, ordinal_position,
       data_type, udt_schema, udt_name, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name, ordinal_position;
```

For keys and relationships, use the appropriate catalogue views or an authorised schema export.
In `pg_constraint`, `conkey` and `confkey` contain ordered column numbers for a foreign key.
Pair their positions and resolve them through `pg_attribute`. Do not join all source columns to all target columns.
Record `convalidated` and available enforcement metadata without treating them as business approval.

`information_schema.table_constraints` can hide constraints from a SELECT-only identity.
Record this as a visibility limit rather than requesting write rights for discovery.
Visible tables and columns also depend on the current identity's privileges.
These limits are documented for [tables](https://www.postgresql.org/docs/current/infoschema-tables.html),
[columns](https://www.postgresql.org/docs/current/infoschema-columns.html), and
[table constraints](https://www.postgresql.org/docs/current/infoschema-table-constraints.html).
See [pg_constraint](https://www.postgresql.org/docs/current/catalog-pg-constraint.html) for native constraint metadata.

## SQLite

Read `sqlite_schema` for definitions. These examples inspect the `main` database.

```sql
SELECT name, type, sql
FROM main.sqlite_schema
WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%'
ORDER BY name;
```

```sql
PRAGMA main.table_xinfo('order_items');
PRAGMA main.foreign_key_list('order_items');
PRAGMA main.index_list('order_items');
PRAGMA main.foreign_keys;
```

Replace the example table with an inspected name. Quote names with the tool's supported identifier rules.
`table_xinfo` includes generated and hidden columns. Read unique index columns through `index_xinfo` when needed.
For foreign keys, group by `id` and order by `seq`. A composite relationship is one edge, not separate joins.
`foreign_keys` without an assignment reads this connection's setting. Do not change it during discovery.
The setting does not prove that all historical rows were checked.
See the [SQLite PRAGMA reference](https://www.sqlite.org/pragma.html).

## Other SQL dialects

Use the existing tool's metadata features or the vendor catalogue. Keep unsupported fields unknown.

- SQL Server: use [system catalogue views](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/catalog-views-transact-sql).
  Resolve foreign key columns through `sys.foreign_key_columns`. Record disabled or untrusted constraints where visible.
- MySQL: use `INFORMATION_SCHEMA` with the correct database scope.
  [KEY_COLUMN_USAGE](https://dev.mysql.com/doc/refman/8.4/en/information-schema-key-column-usage-table.html) gives ordered key columns and referenced names.

Do not run PostgreSQL or SQLite examples on a different dialect.

## Optional data checks

Use data checks only within authorised data-inspection scope. Prefer aggregate results to raw rows.
Useful checks include duplicate candidate keys, null join columns, unmatched references, and row multiplication after a join.
Restrict scans by the supplied scope and tool limits. A bounded sample cannot prove uniqueness or full referential integrity.
Record the exact population and limits for each result. If checks are unavailable, keep those findings unverified.
