# Support Portal — Metric Sources

This is a synthetic example. Project: SP. Outcome: SPOC001 — fewer publishing attempts need developer help.
Metric ID: SPMT001. The supplied dialect is SQLite.

## E1 — Source fields

`input-schema.sql` defines `main.publishing_attempts` and `main.attempt_notes`.
One attempt row represents one publishing attempt within one tenant.
`tenant_id` and `attempt_id` form the primary key. Attempt IDs can repeat across tenants.
`started_at` is canonical UTC text in YYYY-MM-DDTHH:MM:SSZ format.
`needs_help` is 1 for help, 0 for no help, or null for unknown.
Notes are detail rows. There can be several notes for one attempt.

## E2 — Definition decision

Example SME agreed these rules on 2026-11-24 for this synthetic example:

- Count attempts for the authorised tenant with start time in the supplied period.
- Include the start boundary and exclude the end boundary.
- Exclude unknown help flags from numerator and denominator. Report the unknown count separately.
- Numerator: eligible attempts with needs_help = 1. Denominator: attempts with a known flag, 0 or 1.
- Percent: 100 × numerator / denominator. Return null when the denominator is zero.
- Do not join notes into the attempt population.

## E3 — Test scope and target

The synthetic test caller is tenant 1. Period start: 2026-11-02T00:00:00Z. Period end: 2026-11-09T00:00:00Z.
Expected counts: 2 helped, 3 eligible, and 1 unknown. Expected percent: 100 × 2 / 3.
The existing 15% target remains proposed. The historical 30% baseline used all recorded attempts.
Its treatment of unknown flags is not supplied. Comparability with this definition is unconfirmed.
No live database, baseline, access rights, or runtime enforcement has been checked.
