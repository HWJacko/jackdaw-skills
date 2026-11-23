# Example Review — Order Counts

These answers are synthetic fixtures. They do not approve access to a real database.
Project: Query Example | Abbreviation: QE
Respondent: Example SME | Date: 2026-11-23

## QEQ001 — Table meaning and row grain

`main.orders` contains current order records. One row represents one order within one tenant.
`tenant_id` and `order_id` form the primary key. Order IDs may repeat across tenants.
The three columns are `tenant_id INTEGER NOT NULL`, `order_id INTEGER NOT NULL`, and `status TEXT NOT NULL`.

## QEQ002 — Expected query result

Question: "How many orders are in each status for my tenant?"
Count order rows by their exact stored status. Include every status present for the caller's tenant.
The result has one row per status. Return `status` and `order_count`, sorted by status.
Do not return tenant or order IDs. No join is required.
Bind the tenant from the authenticated caller. Do not accept a tenant chosen by the language model.

For tenant 1, the test rows have one `new` order and two `paid` orders.
For tenant 2, the test rows have three `paid` orders.
Tenant 1 must receive `new: 1` and `paid: 2`. Tenant 2 must receive only `paid: 3`.

## Setup limits

The runtime, access owner, time limit, and result limits have not been selected.
The schema handoff is ready for this count query. The runtime setup remains blocked.
