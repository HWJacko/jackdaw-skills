# Shop Analytics — SME Questions

Handoff: needs_confirmation

These seven decisions block the stated query scope. No answers have been supplied.

## SAQ001 — Decision for SATB001, SATB002, SARL002

Priority: blocking | Subjects: SATB001, SATB002, SARL002 | Status: open
Evidence: SAEV001, SAEV002
Question: Do orders link to customers on both tenant_id and customer_id? Can an order refer to a missing or historical customer?
Why it matters: The schema declares no customer foreign key. A customer_id-only join can mix tenants or multiply rows.
Needed evidence: The complete join rule, treatment of unmatched rows, and a cross-tenant example with repeated customer_id values.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ002 — Decision for SATB001, SATB002, SATB003

Priority: blocking | Subjects: SATB001, SATB002, SATB003 | Status: open
Evidence: SAEV001, SAEV002, SAEV003
Question: What does one row represent in each table? Are orders and customers current records, versions, or snapshots?
Why it matters: Physical primary keys do not establish business grain. The wrong grain can double-count revenue.
Needed evidence: A business definition for each table and the rule for historical or deleted records.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ003 — Decision for SATB002

Priority: blocking | Subjects: SATB002 | Status: open
Evidence: SAEV002, SAEV004
Question: Which status values count as paid revenue? How do refunds, cancellations, and partial payments affect that amount?
Why it matters: No status dictionary or payment rule is supplied. A guessed filter can change reported revenue.
Needed evidence: The status dictionary and the agreed revenue calculation with a worked refund example.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ004 — Decision for SATB002

Priority: blocking | Subjects: SATB002 | Status: open
Evidence: SAEV002
Question: What does total_minor measure? Which units, currency rules, taxes, and discounts apply? Can currencies be combined?
Why it matters: The column name does not prove a divisor, a revenue definition, or a valid cross-currency total.
Needed evidence: The amount definition, currency unit rules, and any approved conversion or separate-currency grouping rule.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ005 — Decision for SATB002

Priority: blocking | Subjects: SATB002 | Status: open
Evidence: SAEV002, SAEV004
Question: Which source field and time zone define this month for paid revenue? The supplied tables have no date column.
Why it matters: The intended question requires a period filter that cannot be built from the supplied schema.
Needed evidence: The missing timestamp source, its join rule, the business date definition, and month boundary rules.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ006 — Decision for SATB001, SATB002, SATB003

Priority: blocking | Subjects: SATB001, SATB002, SATB003 | Status: open
Evidence: SAEV001, SAEV002, SAEV003, SAEV004
Question: Which tenants and customer fields may each user access? Where is tenant scope enforced, and may display_name be exposed?
Why it matters: The brief allows users from different tenants. Schema discovery does not establish their access rights.
Needed evidence: The access owner, tenant isolation rule, permitted customer fields, and responsibility for runtime enforcement.
Answer: pending
Answered by: pending
Answered on: pending

## SAQ007 — Decision for SATB001, SATB002, SATB003, SARL001, SARL002

Priority: blocking | Subjects: SATB001, SATB002, SATB003, SARL001, SARL002 | Status: open
Evidence: SAEV001, SAEV002, SAEV003, SAEV004
Question: What result should the target question return for two customers, repeated tenant-local IDs, and an order with several items?
Why it matters: Joining order totals to item rows can multiply revenue. Customer grouping and the expected result need confirmation.
Needed evidence: An SME-approved example with expected totals, result grain, required joins, filters, and currency treatment.
Answer: pending
Answered by: pending
Answered on: pending
