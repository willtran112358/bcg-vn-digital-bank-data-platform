# As-is vs to-be — one-page summary

| Dimension | As-is | To-be (target) |
|-----------|-------|----------------|
| **Platform** | Oracle ODS + Informatica on-prem | Hybrid: Oracle SoR + **AWS lakehouse** |
| **Customer ID** | Multiple IDs per person | **SSOT** + `xref_customer_id` |
| **Income data** | Optional → ~70% null in mart | Source fix + DQ SLA + `declared_*` / `estimated_*` |
| **Ingest** | Nightly batch only | Batch + **MSK streaming** (payments) |
| **Storage** | Oracle marts | **S3 medallion** + **Redshift gold** |
| **DQ** | After BI discovery | **Shift-left** gates silver→gold |
| **Lineage** | Excel | Glue Catalog + `pipeline_run_id` |
| **PII** | Shared drives risk | **Lake Formation** tags + KMS |
| **Digital migration** | Cannot export prod T24 | **Synthetic layer** + recon |
| **Time-to-insight** | Days (IT ticket) | Hours (self-serve on gold views) |

---

## Talking points (interview)

1. **Pilot first (MSB):** Prove AWS pattern on marketing before enterprise cutover — reduces political risk.
2. **Constraint-driven design (TCB):** Synthetic + streaming when prod data cannot leave bank.
3. **Hybrid is permanent:** Oracle stays SoR; cloud is analytics SSOT — not lift-and-shift core.
4. **DQ is product:** Completeness SLAs owned with business, not only engineering tickets.
5. **Regulatory literacy:** Imputation policy differs for marketing vs credit — engineer encodes separation.

---

## Architecture delta (ASCII)

```text
AS-IS:  [Core]──ETL──►[Dept mart]──► BI
TO-BE:  [Core]──► Bronze ──► Silver ──DQ──► Gold/Redshift ──► BI/ML
              └── MSK ──┘
```

---

## 90-day success criteria (example)

- [ ] Landing zone + 3 bronze sources live  
- [ ] `dim_customer` SCD2 v1 in gold  
- [ ] Income completeness dashboard + 1 remediation workflow  
- [ ] Pipeline SLA dashboard; on-call runbook  
- [ ] 1 legacy mart read-only deprecated  
