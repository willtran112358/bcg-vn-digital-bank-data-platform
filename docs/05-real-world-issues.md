# Real-world issues — VN bank ETL, DQ, production & BI

Playbook for interviews and on-call. Patterns from MSB/TCB-style programs and common VN retail bank pain.

---

## 1. Customer data quality

### 1.1 Missing income (~70% null) — flagship case

| Symptom | Dashboard shows tiny "high income" segment |
| Root causes | Optional onboarding field; branch skip; ETL maps NULL→0 inconsistently; CRM not in extract |
| Fix ladder | Measure → segment → mandatory policy for products → RM campaign → pipeline quarantine → **estimated_* column with flag** |
| Do not | Silent ML fill into `declared_income` used for credit |

Detail: [`06-case-missing-customer-income.md`](06-case-missing-customer-income.md)

### 1.2 Duplicate customer / CIF

| Symptom | Same person, 2 loans, different IDs |
| Detection | `national_id` + phone fuzzy match; count >1 current SCD row |
| Fix | Golden ID in `xref_customer_id`; survivorship rules (newest KYC wins) |

### 1.3 MNAR (missing not at random)

Wealthier customers more likely to declare income → segment median imputation **biased**. Always segment analysis before impute.

### 1.4 Unicode / Vietnamese name normalization

| Issue | `Nguyễn` vs `Nguyen` breaks join |
| Fix | Normalization UDF; keep `display_name` raw + `search_name` folded |

---

## 2. Hybrid Oracle ↔ AWS (VN environment)

| Issue | What happens | Mitigation |
|-------|--------------|------------|
| **Extract window clash** | Core EOD 00:00–04:00; extract fails if overlap | Coordinate with DBA; watermark table |
| **VN timezone** | Business date off by 1 vs UTC partition | `Asia/Ho_Chi_Minh` in job params |
| **VPN / DX blip** | Half file on S3 | Checksum + `SUCCESS` marker file; no downstream trigger |
| **NLS / encoding** | Oracle `VARCHAR2` VN charset → mojibake in Parquet | UTF-8 validate in bronze |
| **NUMBER precision** | Amount scale mismatch | Explicit `DECIMAL(18,2)` in silver schema |
| **Long-running JDBC** | Glue job timeout | Chunk by PK range; parallel workers |

---

## 3. Pipeline production incidents

### 3.1 Glue OOM / skew

```
Error: Executor lost heartbeat / OOM
Cause: One hot `customer_id` with millions of events
Fix: Salting, repartition, broadcast small dims only
```

### 3.2 Bookmark / incremental bug

Duplicate rows after redeploy — reset bookmark only with **backfill plan** and idempotent merge.

### 3.3 Partial partition publish

Job writes `dt=2025-05-21` 80% files then fails → BI mixed old/new.

**Pattern:** Write to `.../staging/dt=` then **atomic** copy/commit; or Redshift **merge** in transaction.

### 3.4 Step Functions retry storm

Downstream Redshift WLM queue full → cascade.

**Fix:** Exponential backoff; concurrency limits; dead-letter SNS with runbook link.

### 3.5 MSK consumer lag (TCB-style)

| Symptom | Lag > 30 min; digital validation delayed |
| Actions | Scale consumers; check poison message → DLQ; verify core recon still balances EOD |

---

## 4. BI & reporting incidents

| Incident | Cause | Prevention |
|----------|-------|------------|
| **FX wrong** | Used daily rate table not joined on txn date | Gold test: sum USD eq vs finance control |
| **Duplicate grain** | Fan-out join account×customer | QA query: row count vs source distinct keys |
| **Stale mart** | Pipeline green but wrong partition | Freshness SLA on `max(batch_id)` |
| **Metric definition drift** | Marketing vs risk different "active customer" | Business glossary in catalog |
| **Excel override** | Branch sends "corrected" list outside pipeline | Governance: no production lists outside SSOT |

---

## 5. Governance & compliance

| Issue | Example |
|-------|---------|
| PII in dev bucket | Full prod dump copied to `dev-lake` |
| Imputation in scorecard | Estimated income used for mortgage approve — model risk escalation |
| No audit trail | Cannot answer "who changed income on CIF X?" |
| PDPA | Marketing uses attribute without consent purpose |

**Engineering response:** Lake Formation deny on PII for dev roles; separate columns; lineage_id; consent flag in silver.

---

## 6. Organizational / process

| Anti-pattern | Better |
|--------------|--------|
| "IT said data is ready" without DQ sign-off | Published **data contract** with business owner |
| Consulting builds; bank cannot operate | Runbooks + pair with bank DE |
| Big-bang cutover | MSB-style **domain pilot** |
| Scope creep on T24 mapping | Time-box synthetic layer; formal change request |

---

## 7. Incident response template (copy for runbook)

```markdown
## INC: [title]
- **Severity:** P1/P2
- **Impact:** [mart/table, downstream BI]
- **Detection:** [CloudWatch / user report]
- **Timeline:** start / mitigate / resolve
- **Root cause:** [technical + process]
- **Fix:** [replay partition, hotfix mapping]
- **Follow-up:** DQ rule added? Postmortem date?
```

---

## 8. Interview rapid-fire (English one-liners)

| Question | Answer hook |
|----------|-------------|
| Optional income 70% missing? | Measure, source fix, separate estimated column, policy by use case |
| Prove ETL not culprit? | Hash reconcile source vs bronze vs silver same keys |
| Hybrid Oracle AWS? | SoR on-prem; analytics SSOT cloud; watermark incremental |
| TCB synthetic layer? | Regulatory constraint — realistic volume without prod export |
| Production pipeline failed 6am? | Block gold publish; replay staging; comms to BI before partial data |
