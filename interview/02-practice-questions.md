# Practice questions — CTO / client technical

Repo refs: [`../docs/05-real-world-issues.md`](../docs/05-real-world-issues.md), [`../docs/06-case-missing-customer-income.md`](../docs/06-case-missing-customer-income.md).

Practice **out loud in English**. Target **2–3 minutes** per answer.

---

## A. Case — missing income & DQ

1. Walk through your approach when **70% of customers lack income**.  
2. How do you detect whether missingness is **MNAR**?  
3. Design warehouse columns for **declared vs estimated** income.  
4. Would you use imputed income in **credit scorecard**?  
5. DQ rule: mortgage onboarding requires income within 24h — how implement?  
6. Branch officers skip optional fields — fix **process** vs **technology**?  
7. Reconcile **CRM income** vs **core banking income** mismatch?  
8. KPIs for CDO after 90 days?

**Skeleton (Q1):** Measure → segment → root cause → source remediation → DQ gates → flagged estimates → governance by use case.

---

## B. SQL / modeling

9. SCD2 update when income changes → see [`../samples/dim_customer_scd2.sql`](../samples/dim_customer_scd2.sql)  
10. Gold null but CRM has income → see [`../samples/dq_income_completeness.sql`](../samples/dq_income_completeness.sql)  
11. Dedup same `national_id`, different `customer_id`  
12. Monthly snapshot fact with last known income  
13. Fill rate trend by onboarding month  
14. Detect completeness drop after release  

---

## C. AWS / pipelines

15. Glue vs Lambda vs EMR — when each?  
16. Idempotent daily customer load from S3  
17. Step Functions: ingest → DQ → gold  
18. Late-arriving customer updates in streaming  
19. PII security: IAM, KMS, Lake Formation  
20. Redshift + Glue cost drivers  

---

## D. Banking domain

21. **T24** and synthetic layer — [`../cases/tcb-digital-streaming-layer.md`](../cases/tcb-digital-streaming-layer.md)  
22. Onboarding KYC income vs annual review  
23. **~1–2M checks/day** architecture impact  
24. Core SoR vs warehouse SSOT boundaries  
25. Consulting scope change mid-sprint  

---

## E. System design

26. Customer 360 on AWS — [`../docs/03-to-be-architecture.md`](../docs/03-to-be-architecture.md)  
27. Real-time fraud features + batch DWH  
28. Group bank central DWH vs VN mart  
29. Alert when income completeness SLO breached  
30. Backfill 5y historical income after bureau feed  

---

## F. Behavioral / senior

31. SCD1 vs SCD2 disagreement with client architect  
32. Gold mart wrong currency — incident story  
33. Mentor junior on DQ testing  
34. Saying **no** to go-live  
35. Why this consulting + bank project  

---

## Sample answer — Q4 (imputation in credit)

```text
Default: declared or bureau-verified income for credit decisions.
Imputation is biased when missingness correlates with wealth — common with optional fields.
If allowed at all, scope to pre-screen only, store in estimated_* with model version,
require risk sign-off; final decision uses verification, not silent fill.
```

---

## Mock 60-minute script

| Min | Activity |
|-----|----------|
| 0–5 | Intro from `01-cto-round-prep.md` |
| 5–20 | MSB STAR + drill |
| 20–35 | Missing income case |
| 35–45 | Whiteboard to-be architecture |
| 45–55 | SQL 9, 10, 13 |
| 55–60 | Questions for CTO |

**Target:** self-score ≥ 4/5 on clarity, AWS, SQL, compliance before real call.
