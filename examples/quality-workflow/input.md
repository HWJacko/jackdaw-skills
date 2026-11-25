# Evidence Check — Worked-Example Input

This is a synthetic brief. Project abbreviation: EC. All people, decisions, and data are fictional.
Assess the workflow with missing evidence and conflicting rules. No target application or live database is supplied.

## ECEV001 — Research session A

Participant P1 cannot tell which attempts are included in the help-rate denominator.
This is one participant in a two-person exploratory round.

## ECEV002 — Research session B

Participant P2 cannot explain what happens when the help flag is unknown.
Recruitment and population coverage are not supplied. These notes are not representative market evidence.

## Task and outcome

An analyst should be able to inspect a help-rate report for the authorised tenant and understand its population.
No baseline, target, deadline, capacity, or named release owner is supplied.

## Recorded rules

The Example Data Owner supplies these current rules:

- With an authorised tenant parameter, the query population must contain only attempts for that tenant.
- An empty eligible population must produce an unavailable rate, not 0%.

## Conflicting requests

The Example Business Owner says unknown help flags must be excluded from the denominator.
The Example Reporting Manager says they must count as no help.
No decision resolves these conflicting requests. The brief also says the report should be "fast", without a measurable bound.

## Supplied test setting

`fixture.sql` defines synthetic attempts. Tenant-local attempt IDs repeat across tenants.
The permitted local exercise is to check the query population for trusted parameter tenant_id = 1.
This does not test caller authentication, server permissions, the whole metric, or a target application.
Other acceptance cases have not run. Do not create passing results for them.
