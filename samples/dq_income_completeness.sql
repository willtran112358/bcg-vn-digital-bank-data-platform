-- Data quality: income completeness by segment + SLA breach detection
-- Run after silver/gold load; feed results to CloudWatch custom metric or alerting table

-- Overall completeness (current customers)
SELECT
    COUNT(*) AS total_customers,
    COUNT(declared_income_amount) AS with_income,
    ROUND(100.0 * COUNT(declared_income_amount) / NULLIF(COUNT(*), 0), 2) AS pct_complete
FROM gold.dim_customer
WHERE is_current = TRUE
  AND customer_status = 'ACTIVE';

-- By onboarding channel (find MNAR patterns)
SELECT
    onboarding_channel,
    COUNT(*) AS n,
    COUNT(declared_income_amount) AS with_income,
    ROUND(100.0 * COUNT(declared_income_amount) / NULLIF(COUNT(*), 0), 2) AS pct_complete
FROM gold.dim_customer
WHERE is_current = TRUE
GROUP BY 1
ORDER BY pct_complete ASC;

-- 7-day fill rate for new onboardings (SLA example: 85%)
WITH onboard AS (
    SELECT
        customer_id,
        onboarding_channel,
        valid_from AS onboard_date,
        declared_income_amount
    FROM gold.dim_customer
    WHERE is_current = TRUE
      AND valid_from >= CURRENT_DATE - 30
)
SELECT
    onboarding_channel,
    COUNT(*) AS onboarded_30d,
    SUM(CASE WHEN declared_income_amount IS NOT NULL THEN 1 ELSE 0 END) AS with_income,
    ROUND(100.0 * SUM(CASE WHEN declared_income_amount IS NOT NULL THEN 1 ELSE 0 END)
          / NULLIF(COUNT(*), 0), 2) AS pct_complete
FROM onboard
GROUP BY 1
HAVING pct_complete < 85.0;  -- SLA breach candidates

-- Reconciliation: gold null but CRM source had value (pipeline bug detector)
-- Requires staging or bronze CRM snapshot crm.customer_income_stg
SELECT
    g.customer_id,
    g.declared_income_amount AS gold_income,
    c.income_amount AS crm_income
FROM gold.dim_customer g
JOIN stg.crm_customer_income c ON g.customer_id = c.customer_id
WHERE g.is_current = TRUE
  AND g.declared_income_amount IS NULL
  AND c.income_amount IS NOT NULL
LIMIT 100;

-- DQ alert insert (pattern)
/*
INSERT INTO ops.dq_alert (rule_id, severity, metric_value, threshold, created_ts)
SELECT 'INCOME_COMPLETENESS_MORTGAGE', 'CRITICAL', pct_complete, 95.0, GETDATE()
FROM (... mortgage cohort query ...);
*/
