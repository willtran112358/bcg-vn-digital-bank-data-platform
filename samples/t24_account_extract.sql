-- T24 / Temenos core banking extract — account & customer domain
-- Hybrid pattern: JDBC extract to S3 bronze (Glue) or sqlplus unload
-- Watermark: etl_ctrl.extract_watermark WHERE entity_name = 'T24_FBNK_CUSTOMER'

SELECT
    c.CUSTOMER_NO,
    c.SHORT_NAME,
    c.NAME_1,
    c.NAME_2,
    c.SECTOR,
    c.INDUSTRY,
    c.TARGET,
    c.NATIONALITY,
    c.RESIDENCE,
    c.DATE_OF_BIRTH,
    c.PHONE_1,
    c.EMAIL_1,
    c.AML_CHECK,
    c.KYC_COMPLETE,
    c.RECORD_STATUS,
    c.CURR_NO,
    c.INPUTTER,
    c.DATE_TIME,
    'T24_CORE' AS source_system,
    SYSTIMESTAMP AT TIME ZONE 'UTC' AS extract_ts
FROM FBNK_CUSTOMER c
WHERE c.RECORD_STATUS = 'LIV'
  AND c.DATE_TIME > :last_watermark
  AND c.DATE_TIME <= :max_ts
ORDER BY c.DATE_TIME, c.CUSTOMER_NO;

-- Account balance snapshot (daily EOD — coordinate with T24 COB window)
SELECT
    a.ACCOUNT_NO,
    a.CUSTOMER_NO,
    a.CURRENCY,
    a.ACCOUNT_TITLE_1,
    a.CATEGORY,
    a.OPENING_DATE,
    a.WORKING_BALANCE,
    a.ONLINE_ACTUAL_BAL,
    a.RECORD_STATUS,
  a.DATE_TIME
FROM FBNK_ACCOUNT a
WHERE a.RECORD_STATUS = 'LIV'
  AND a.DATE_TIME >= TRUNC(SYSDATE) - 1;
