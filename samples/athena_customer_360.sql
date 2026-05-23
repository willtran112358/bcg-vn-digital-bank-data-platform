-- PROPOSED: Athena BI layer on S3 Gold / Silver (serverless analytics)
-- Glue Catalog database: bank_gold
-- Typical MSB marketing pilot / TCB digital reporting pattern

-- 1) Customer 360 view for marketing segmentation (declared vs estimated income)
CREATE OR REPLACE VIEW bank_gold.v_customer_360 AS
SELECT
    c.customer_id,
    c.cif_number,
    c.full_name,
    c.onboarding_channel,
    c.branch_code,
    c.customer_status,
    c.declared_income_amount,
    c.declared_income_currency,
    c.estimated_income_amount,
    c.is_imputed,
    c.income_confidence,
    CASE
        WHEN c.declared_income_amount IS NOT NULL THEN 'DECLARED'
        WHEN c.is_imputed = TRUE THEN 'ESTIMATED'
        ELSE 'UNKNOWN'
    END AS income_data_quality_band,
    a.active_account_count,
    a.total_balance_vnd,
    c.valid_from,
    c.is_current,
    c.pipeline_run_id,
    c.business_date
FROM bank_gold.dim_customer c
LEFT JOIN (
    SELECT
        customer_id,
        COUNT(DISTINCT account_no) AS active_account_count,
        SUM(CASE WHEN currency = 'VND' THEN balance ELSE 0 END) AS total_balance_vnd
    FROM bank_silver.account_daily
    WHERE account_status = 'ACTIVE'
      AND business_date = (SELECT MAX(business_date) FROM bank_silver.account_daily)
    GROUP BY customer_id
) a ON c.customer_id = a.customer_id
WHERE c.is_current = TRUE;

-- 2) Income completeness KPI for DQ dashboard (QuickSight / Athena)
SELECT
    onboarding_channel,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN declared_income_amount IS NOT NULL THEN 1 ELSE 0 END) AS with_declared_income,
    ROUND(100.0 * SUM(CASE WHEN declared_income_amount IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS fill_rate_pct
FROM bank_gold.v_customer_360
GROUP BY onboarding_channel
ORDER BY fill_rate_pct ASC;

-- 3) Partition pruning example — always filter business_date on bronze/silver
SELECT customer_id, full_name, declared_income_amount
FROM bank_silver.customer
WHERE business_date = DATE '2025-05-21'
  AND onboarding_channel = 'MOBILE_APP'
  AND declared_income_amount IS NULL
LIMIT 100;
