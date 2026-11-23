# Query Example — Query Access

Status: draft | Owner: unknown
Scope: order counts by status for the authenticated tenant
Runtime: unknown

| Control | Required rule | Enforcement point | Owner | Test | Result |
| --- | --- | --- | --- | --- | --- |
| Objects and fields | Read `main.orders`. Return only status and order_count. Use tenant_id for scope. | database and query path | unknown | QEQT001–QEQT003 | not_run |
| Joins | No joins are approved for this scope. | query path | unknown | QEQT004 | not_run |
| Identity and tenant scope | Bind tenant_id from trusted caller identity. Reject a tenant override. | authentication and query path | unknown | QEQT002–QEQT003 | not_run |
| Read-only execution | No writes, extra statements, or unapproved functions. | database and query path | unknown | QEQT005 | not_run |
| Query limits | Timeout, returned rows, and output size remain unknown. | runtime | unknown | QEQT006 | not_run |
| Secrets and logs | Use secret references. Exclude credentials and raw personal values from logs. | runtime | unknown | QEQT007 | not_run |

The synthetic SME answers define the intended result. They do not prove runtime enforcement.
No database connection has been made for this example.
