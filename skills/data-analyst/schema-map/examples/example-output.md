# Shop Analytics — Assumed Schema Map

Date: 2026-11-23 | Project: SA | Handoff: needs_confirmation

## Source and limits

Source: supplied SQLite DDL in `input-schema.sql` and the scope in `input-brief.md`.

- Supplied DDL only. No live database or business rows were inspected.
- No SME answers or data-quality checks are available.
- A foreign key declaration does not prove enforcement or valid historical data.
- The supplied schema has no date column for the requested month filter.

## Tables and row grain

| ID | Database object | Observed structure | Proposed meaning and grain | Status | Evidence | Questions |
| --- | --- | --- | --- | --- | --- | --- |
| SATB001 | main.customers | 3 NOT NULL columns; PK (tenant_id, customer_id) | Customer records within a tenant. One row may represent one current customer within one tenant. | assumed meaning and grain | SAEV001 | SAQ002 |
| SATB002 | main.orders | 6 NOT NULL columns; PK (tenant_id, order_id) | Orders placed by customers within a tenant. One row may represent one order within one tenant. | assumed meaning and grain | SAEV002 | SAQ002 |
| SATB003 | main.order_items | 3 NOT NULL columns; PK (tenant_id, order_id, line_number) | Lines within an order. One row may represent one order line within one tenant. | assumed meaning and grain | SAEV003 | SAQ002 |

## Columns

| Object | Column | Type | Nullable | Evidence |
| --- | --- | --- | --- | --- |
| main.customers | tenant_id | INTEGER | no | SAEV001 |
| main.customers | customer_id | INTEGER | no | SAEV001 |
| main.customers | display_name | TEXT | no | SAEV001 |
| main.orders | tenant_id | INTEGER | no | SAEV002 |
| main.orders | order_id | INTEGER | no | SAEV002 |
| main.orders | customer_id | INTEGER | no | SAEV002 |
| main.orders | status | TEXT | no | SAEV002 |
| main.orders | total_minor | INTEGER | no | SAEV002 |
| main.orders | currency_code | TEXT | no | SAEV002 |
| main.order_items | tenant_id | INTEGER | no | SAEV003 |
| main.order_items | order_id | INTEGER | no | SAEV003 |
| main.order_items | line_number | INTEGER | no | SAEV003 |

## Relationships

| ID | Ordered source columns | Ordered target columns | Cardinality | Status | Query use | Evidence | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SARL001 | main.order_items (tenant_id, order_id) | main.orders (tenant_id, order_id) | declared many-to-one | observed | blocked | SAEV002, SAEV003 | SAQ002, SAQ007 |
| SARL002 | main.orders (tenant_id, customer_id) | main.customers (tenant_id, customer_id) | candidate many-to-one | assumed | blocked | SAEV001, SAEV002 | SAQ001, SAQ007 |

## Business meanings and query cases

- main.orders.status: unknown Status: unknown. Questions: SAQ003.
- main.orders.total_minor: The value may be an order total in currency minor units. Status: assumed. Questions: SAQ003, SAQ004.
- main.orders.currency_code: The value may identify the currency of total_minor. Status: assumed. Questions: SAQ004.
- Month filter: unknown Status: unknown. Questions: SAQ005.
- Tenant and field access: unknown Status: unknown. Questions: SAQ006.

Question: What was paid revenue by customer this month?
Candidate plan: use orders at confirmed order grain; join customers on both tenant_id and customer_id. Do not join item rows unless the agreed measure requires them. Group by the confirmed customer identity and currency rule. Paid status, amount calculation, date source, period boundary, tenant access, and expected totals remain unconfirmed. Do not execute this plan.
Status: assumed. Evidence: SAEV001–SAEV004. Questions: SAQ001–SAQ007.

## Handoff decision

Open blocking questions: SAQ001, SAQ002, SAQ003, SAQ004, SAQ005, SAQ006, SAQ007.
The model is not ready for a text-to-SQL handoff. The SME must confirm the business rules and query acceptance case.
Runtime controls: not_assessed
No SME answers have been supplied.

## Evidence

| ID | Source | Finding |
| --- | --- | --- |
| SAEV001 | input-schema.sql:1-6 | Customer columns and the ordered tenant_id, customer_id primary key. |
| SAEV002 | input-schema.sql:8-16 | Order columns and primary key. No customer foreign key or date column is declared here. |
| SAEV003 | input-schema.sql:18-25 | Order item columns, primary key, and ordered composite foreign key to orders. |
| SAEV004 | input-brief.md | The intended question is paid revenue by customer this month. Users may belong to different tenants. |
