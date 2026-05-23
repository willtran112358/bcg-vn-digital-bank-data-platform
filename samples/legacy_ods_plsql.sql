-- =============================================================================
-- AS-IS: Legacy on-prem ODS load (Informatica / PL-SQL style)
-- Typical VN retail bank before cloud migration — department silo, no DQ gate
-- =============================================================================

-- Nightly job: merge CRM export into dept marketing ODS (simplified)
CREATE OR REPLACE PROCEDURE mkt_ods.load_customer_daily AS
BEGIN
    MERGE INTO mkt_ods.customer c
    USING (
        SELECT
            crm.party_id          AS customer_id,   -- NOT same as core CIF
            crm.full_name,
            crm.phone,
            NVL(crm.annual_income, 0) AS income,     -- NULL → 0 silently (DQ bug)
            crm.last_modified
        FROM crm_export.customer_stg crm
        WHERE crm.last_modified >= TRUNC(SYSDATE) - 1
    ) s
    ON (c.customer_id = s.customer_id)
    WHEN MATCHED THEN UPDATE SET
        c.full_name = s.full_name,
        c.income    = s.income,
        c.updated   = SYSDATE
    WHEN NOT MATCHED THEN INSERT (customer_id, full_name, phone, income, updated)
    VALUES (s.customer_id, s.full_name, s.phone, s.income, SYSDATE);

    COMMIT;
    -- No watermark table, no lineage, no quarantine, no _SUCCESS marker
END;
/

-- Pain points this pattern causes:
-- 1) CRM party_id ≠ core CIF → duplicate customers in BI
-- 2) NVL(income, 0) → false "zero income" segment in Tableau
-- 3) No extract window coordination with core EOD batch
-- 4) No audit columns for NHNN / internal audit lineage
