# Consulting DE — 1-page cheat sheet (print / mobile)

> **BCG VN Digital Bank Transform** · Hybrid Oracle/T24 → AWS · MSB + TCB patterns  
> Full scripts: [`05-consulting-de-client-communication.md`](05-consulting-de-client-communication.md)

---

## A. 60-second pitch

> Consulting data engineer — hybrid banking ETL, SSOT, DQ gates, streaming under regulatory constraints. I match the technical scope (Glue, Redshift, Athena, governance). I deliver at consulting level: proactive updates, business-framed issues, clear options plus recommendation, same-day BA/PO alignment, closed loops until stakeholders are satisfied.

---

## B. Technical proof (point to repo)

| Say | Evidence |
|-----|----------|
| Hybrid extract, COB-aware | `oracle_extract_customer.sql`, `t24_account_extract.sql` |
| No silent NULL→0 | `glue_customer_bronze_to_silver.py` |
| SSOT + income policy | `dim_customer_scd2.sql` (declared vs estimated) |
| DQ blocks gold | `dq_contract.py` |
| Pilot / streaming | `cases/msb-*`, `cases/tcb-*` |

**One-liner:** *Seventy percent missing income → measure → source fix → imputation policy → separate columns — not NVL in legacy ETL.*

---

## C. Communication (address feedback)

| Do | Don't |
|----|-------|
| Daily 3-bullet status to PO/BA | Wait to be asked |
| Impact + Option A/B + recommend + ETA | "Job failed" only |
| Escalate same day if gold at risk | Fix in silo |
| Close loop after fix | Disappear until demo |

**Acknowledge (1 sentence):** *I understand consulting requires more proactive client relationship — I am raising that bar alongside technical delivery.*

---

## D. Ready scripts

**Stand-up (3 bullets):**  
1) Risk: ___ · 2) Decision needed from PO: ___ · 3) ETA gold publish: ___

**Missing source:**  
> CRM income missing — mart blocked in 48h. Plan A: silver CORE_ONLY + flag. Plan B: PO escalate core. Recommend A for MVP; need decision today.

**DQ CRITICAL:**  
> Reconciled root cause. No gold until BA sign-off. Fix + backfill ETA: ___ days. One-pager to PO by 5pm.

**Steering (30s):**  
> Green on SLA. Amber: ___ — impact ___. Interim approach ___. PO decision by ___ to protect Friday publish.

---

## E. Incident loop

`Detect` → `Business impact` → `2 options + recommend` → `Align BA/PO today` → `Fix` → `Close loop`

---

## F. Questions to ask client

1. SoR for income — core, CRM, or onboarding?  
2. Can estimated income be used for marketing vs credit?  
3. Batch T+1 or near-real-time for customer attributes?  
4. Who signs gold go/no-go — PO or Compliance?  
5. 90-day success metric for this program?

---

## G. 30-day commitment

| Week | You will show |
|------|----------------|
| 1 | Stakeholder map + RACI confirmed with PO |
| 2 | Daily proactive status (not reactive) |
| 3 | Lead one data triage / RAID item |
| 4 | One exec slide: green / amber / red |

---

*Print: fit to 1 page · Landscape optional*
