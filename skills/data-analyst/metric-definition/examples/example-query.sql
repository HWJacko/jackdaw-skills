-- SQLite fixture query only. Bind the authorised tenant through the selected runtime.
-- This query does not grant access or prove runtime enforcement.
WITH scoped_attempts AS (
    SELECT needs_help
    FROM main.publishing_attempts
    WHERE tenant_id = :tenant_id
      AND started_at >= :period_start
      AND started_at < :period_end
), counts AS (
    SELECT COUNT(CASE WHEN needs_help = 1 THEN 1 END) AS helped_attempts,
           COUNT(CASE WHEN needs_help IN (0, 1) THEN 1 END) AS eligible_attempts,
           COUNT(CASE WHEN needs_help IS NULL THEN 1 END) AS unknown_attempts
    FROM scoped_attempts
)
SELECT helped_attempts, eligible_attempts, unknown_attempts,
       100.0 * helped_attempts / NULLIF(eligible_attempts, 0) AS help_rate_percent
FROM counts;
