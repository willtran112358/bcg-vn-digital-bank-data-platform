# Case: MSB — Marketing AWS pilot (BCG engagement)

> Anonymized pattern from consulting-led **cloud-first marketing analytics** pilot at Maritime Bank (MSB).

---

## 1. Context

| Item | Detail |
|------|--------|
| Client | MSB — retail bank, Vietnam |
| Partner | Strategy consulting (BCG) + implementation squad |
| Trigger | Marketing needed faster analytics; enterprise core migration too slow |
| Strategy | **Small pattern first** — one domain on AWS before bank-wide lake |

---

## 2. Business problem

| Pain | Detail |
|------|--------|
| Slow insight | Each campaign needed IT extract ticket (days) |
| On-prem limit | Oracle CPU saturated during EOD |
| Fragmented data | CRM + core + agency Excel |
| Cloud appetite | ExCo approved **AWS pilot** for non-ledger analytics |

**Outcome goal:** Marketing team self-serve dashboards on cloud marts with governed PII.

---

## 3. Scope (pilot)

| In scope | Out of scope (phase 1) |
|----------|------------------------|
| Marketing customer & campaign tables | Full enterprise SSOT |
| Glue ETL batch nightly | Real-time payments |
| S3 + modeled marts (Redshift-class) | Core T24 write-back |
| Workshops with MSB marketing + IT | Mobile app feature store |

---

## 4. Architecture (pilot)

```text
Oracle CRM / core (read-only extracts)
    → Glue JDBC / scheduled jobs
    → S3 bronze (marketing entities)
    → Glue transform
    → S3 silver / Redshift gold (mkt_*)
    → QuickSight / Tableau (marketing role)
```

---

## 5. Technical decisions

| Decision | Rationale |
|----------|-----------|
| AWS Glue over Informatica for pilot | Faster iteration; bank building cloud skills |
| Department mart prefix `mkt_` | Clear boundary until SSOT exists |
| Workshop-driven requirements | Marketing defines metrics; DE encodes in SQL |
| PII subset only | Minimize NHNN/PDPA scope in cloud |

---

## 6. Delivery activities

- Source inventory with MSB data owners  
- Mapping workshops (metric definitions)  
- Glue job templates (reused for later domains)  
- UAT with marketing analysts on sample campaigns  
- Handover runbook + training session  

---

## 7. Results (representative)

| Result | Signal |
|--------|--------|
| Pilot live | Marketing queries cloud marts in production |
| Feedback loop | Iterative workshops improved metric trust |
| Reuse | Patterns adopted for other MSB analytics streams |
| Parallel work | Other squads (e.g. mobile) on separate tracks |

*Add your real metrics: tables count, row volumes, timeline, team size.*

---

## 8. Lessons for KUP / similar JD

1. **Pilot reduces risk** — same JD "Data Enhancement" can start domain-by-domain.  
2. **Consulting + bank IT pairing** — daily sync with client data owner.  
3. **Document journeys** — JD asks for "complex data journeys"; marketing CIF→segment is a good story.  
4. **Don't skip DQ** even in pilot — null income breaks campaign ROI models.

---

## 9. Interview STAR

| | |
|-|-|
| **S** | MSB marketing blocked on IT extracts; bank exploring AWS |
| **T** | Deliver cloud ETL + marts for marketing analytics pilot |
| **A** | Glue pipelines, modeled tables, workshops, PII controls |
| **R** | Production pilot; marketing self-serve; foundation for wider program |
