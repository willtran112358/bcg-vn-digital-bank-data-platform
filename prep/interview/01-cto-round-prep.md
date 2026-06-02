# CTO round prep — VN retail bank AWS migration case

Answer in **English**. Repo refs: [`../../docs/`](../../docs/), [`../../samples/`](../../samples/).

Full detail: same as SotaTek pack, paths updated for this repo.

---

## 90-second intro

```text
I'm Will — senior data engineer, ~6 years, focused on banking in Vietnam and APAC consulting.

I build batch and streaming pipelines from Oracle core and channel systems into AWS lakehouse
and Redshift gold marts, with emphasis on customer data quality and stable SLAs.

Recent work: MSB marketing AWS pilot with Glue ETL (BCG program), and Techcombank digital
layer — synthetic T24 staging plus Kafka for about one to two million daily payment checks.

I'm strongest on customer SSOT, hybrid Oracle↔AWS ingest, and cases like optional income
fields with seventy percent missing — source remediation, DQ gates, declared vs estimated columns.
```

---

## STAR — MSB

See [`../../cases/msb-marketing-aws-pilot.md`](../../cases/msb-marketing-aws-pilot.md).

## STAR — TCB

See [`../../cases/tcb-digital-streaming-layer.md`](../../cases/tcb-digital-streaming-layer.md).

## Case — missing income

See [`../../docs/06-case-missing-customer-income.md`](../../docs/06-case-missing-customer-income.md).

## Whiteboard

See [`../../docs/03-to-be-architecture.md`](../../docs/03-to-be-architecture.md) mermaid diagram.

## Questions for CTO

1. System-of-record for income — core, CRM, or onboarding app?  
2. Batch nightly vs near-real-time customer attributes?  
3. Missing income blocking credit, marketing, or regulatory?  
4. Existing DQ — dbt, GX, custom SQL?  
5. 90-day success metric?

## Code to cite live

- `samples/glue_customer_bronze_to_silver.py` — lineage + quarantine  
- `samples/dq_contract.py` — CRITICAL vs WARNING gates  
- `samples/dim_customer_scd2.sql` — income change SCD2  
