-- Incremental Oracle extract: retail customer delta (hybrid pattern)
-- Run from: Glue JDBC job, Airflow OracleOperator, or sqlplus + unload to CSV
-- Business TZ: Asia/Ho_Chi_Minh
-- Watermark table: etl_ctrl.extract_watermark (entity_name, last_success_ts, last_pk_high)

-- Bind :last_ts from watermark; :max_ts usually SYSTIMESTAMP at job start
SELECT
    c.customer_id,
    c.cif_number,
    c.full_name,
    c.national_id,
    c.date_of_birth,
    c.phone_mobile,
    c.email,
    c.occupation_code,
    c.declared_income_amount,
    c.declared_income_currency  AS income_currency,
    c.onboarding_channel,
    c.branch_code,
    c.customer_status,
    c.created_ts,
    c.last_update_ts,
    -- audit for lineage
    'ORACLE_CORE'           AS source_system,
    SYSTIMESTAMP AT TIME ZONE 'UTC' AS extract_ts
FROM core.retail_customer c
WHERE c.last_update_ts > :last_ts
  AND c.last_update_ts <= :max_ts
  AND c.customer_status IN ('ACTIVE', 'DORMANT')
ORDER BY c.last_update_ts, c.customer_id;

-- 3) Chunked extract for very large tables (avoid long locks)
SELECT /*+ PARALLEL(c, 4) */
    c.customer_id,
    c.last_update_ts
FROM core.retail_customer c
WHERE c.customer_id BETWEEN :pk_low AND :pk_high
  AND c.last_update_ts > :last_ts;

-- 4) Post-extract: update watermark (single transaction with job success)
/*
UPDATE etl_ctrl.extract_watermark
SET last_success_ts = :max_ts,
    last_pk_high    = NULL
WHERE entity_name = 'RETAIL_CUSTOMER';
COMMIT;
*/

-- 5) Unload to S3 (pattern — use Glue or external table in practice)
-- sqlplus spool → gzip → aws s3 cp, or Oracle DATAPUMP with policy approval
