-- Redshift: SCD Type 2 merge when declared income changes
-- Assumes staging table stg.dim_customer_daily from silver load

BEGIN TRANSACTION;

-- 1) Close current rows where income (or tracked attrs) changed
UPDATE gold.dim_customer d
SET
    valid_to   = CURRENT_DATE - 1,
    is_current = FALSE,
    updated_ts = GETDATE()
FROM stg.dim_customer_daily s
WHERE d.customer_id = s.customer_id
  AND d.is_current = TRUE
  AND (
        d.declared_income_amount IS DISTINCT FROM s.declared_income_amount
     OR d.declared_income_currency IS DISTINCT FROM s.declared_income_currency
     OR d.phone_mobile IS DISTINCT FROM s.phone_mobile
     OR d.customer_status IS DISTINCT FROM s.customer_status
  );

-- 2) Insert new current version (new SK)
INSERT INTO gold.dim_customer (
    customer_sk,
    customer_id,
    cif_number,
    full_name,
    national_id,
    phone_mobile,
    declared_income_amount,
    declared_income_currency,
    declared_income_as_of,
    declared_income_source,
    estimated_income_amount,
    is_imputed,
    onboarding_channel,
    branch_code,
    customer_status,
    valid_from,
    valid_to,
    is_current,
    pipeline_run_id,
    created_ts,
    updated_ts
)
SELECT
    (SELECT COALESCE(MAX(customer_sk), 0) FROM gold.dim_customer) + ROW_NUMBER() OVER (ORDER BY s.customer_id),
    s.customer_id,
    s.cif_number,
    s.full_name,
    s.national_id,
    s.phone_mobile,
    s.declared_income_amount,
    s.declared_income_currency,
    CASE WHEN s.declared_income_amount IS NOT NULL THEN CURRENT_DATE END,
    s.source_system,
    NULL,  -- estimated only from separate job
    FALSE,
    s.onboarding_channel,
    s.branch_code,
    s.customer_status,
    CURRENT_DATE,
    DATE '9999-12-31',
    TRUE,
    s.pipeline_run_id,
    GETDATE(),
    GETDATE()
FROM stg.dim_customer_daily s
LEFT JOIN gold.dim_customer d
  ON d.customer_id = s.customer_id AND d.is_current = TRUE
WHERE d.customer_id IS NULL  -- brand new customer
   OR d.declared_income_amount IS DISTINCT FROM s.declared_income_amount
   OR d.declared_income_currency IS DISTINCT FROM s.declared_income_currency
   OR d.phone_mobile IS DISTINCT FROM s.phone_mobile
   OR d.customer_status IS DISTINCT FROM s.customer_status;

COMMIT;

-- Freshness check for BI
SELECT MAX(updated_ts) AS dim_customer_last_refresh FROM gold.dim_customer;
