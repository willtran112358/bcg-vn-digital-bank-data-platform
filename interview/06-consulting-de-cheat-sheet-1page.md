# Consulting DE — 1-page cheat sheet (print / mobile)

> **BCG VN Digital Bank Transform** · Hybrid Oracle/T24 → AWS · MSB + TCB patterns  
> Full scripts: [`05-consulting-de-client-communication.md`](05-consulting-de-client-communication.md)

---

## A. 60-second pitch (say this first)

**VN:** Em là DE consulting banking — hybrid Oracle/T24 lên AWS, customer SSOT, DQ shift-left, streaming. Kỹ thuật phù hợp scope (Glue, Redshift, Athena, governance). Khách consulting cần deliver tư vấn: em chủ động báo risk sớm, frame business impact, đưa 2 options + recommend, align BA/PO trong ngày, close loop đến khi PO hài lòng.

**EN:** Consulting data engineer — hybrid banking ETL, SSOT, DQ gates, streaming under regulatory constraints. I match the technical scope and I operate at consulting level: proactive updates, business-framed issues, clear options, same-day BA/PO alignment.

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

**Acknowledge (1 sentence):** *Em hiểu consulting cần chủ động hơn trong client relationship — em đang nâng mức đó song song với delivery kỹ thuật.*

---

## D. Ready scripts (copy tone)

**Stand-up (3 bullets):**  
1) Risk: ___ · 2) Decision needed from PO: ___ · 3) ETA gold publish: ___

**Missing source:**  
> CRM income missing — mart blocked in 48h. Plan A: silver CORE_ONLY + flag. Plan B: PO escalate core. Recommend A for MVP; need decision today.

**DQ CRITICAL:**  
> Reconciled root cause. No gold until BA sign-off. Fix + backfill ETA: ___ days. One-pager to PO by 5pm.

**Steering (30s EN):**  
> Green on SLA. Amber: ___ — impact ___. Interim approach ___. PO decision by ___ to protect Friday publish.

---

## E. Incident loop (remember order)

`Detect` → `Business impact` → `2 options + recommend` → `Align BA/PO today` → `Fix` → `Close loop`

---

## F. Questions to ask client (show consulting mindset)

1. SoR for income — core, CRM, or onboarding?  
2. Can estimated income be used for marketing vs credit?  
3. Batch T+1 or near-real-time for customer attributes?  
4. Who signs gold go/no-go — PO or Compliance?  
5. 90-day success metric for this program?

---

## G. 30-day commitment (if they ask "what will you improve?")

| Week | You will show |
|------|----------------|
| 1 | Stakeholder map + RACI confirmed with PO |
| 2 | Daily proactive status (not reactive) |
| 3 | You lead one data triage / RAID item |
| 4 | One exec slide: green / amber / red |

---

*Print: fit to 1 page · Landscape optional · Repo: willtran112358/bcg-vn-digital-bank-data-platform*
