# KUP Partner JD — mapping to this repo

**Role:** Senior Data Engineer — Data Enhancement, retail banking, hybrid Oracle + AWS  
**Location:** Hanoi hybrid / client site

---

## Responsibilities ↔ evidence

| JD responsibility | Repo pointer |
|-------------------|--------------|
| ETL/ELT hybrid Oracle & AWS | `samples/oracle_extract_customer.sql`, `samples/airflow_hybrid_etl_dag.py` |
| AWS native pipelines | `docs/03-to-be-architecture.md`, `samples/glue_customer_bronze_to_silver.py` |
| Ingestion automation | Airflow DAG, Glue bookmarks pattern in docs |
| Monitoring & alerting | `samples/dq_contract.py`, `docs/05-real-world-issues.md` §3 |
| Document data journeys | `cases/msb-*`, `cases/tcb-*`, `docs/02-as-is-architecture.md` |
| Lake/lakehouse S3 Glue LF | `docs/03-to-be-architecture.md` |
| Redshift DWH | `samples/dim_customer_scd2.sql` |
| SSOT customer | `docs/06-case-missing-customer-income.md`, ER in to-be doc |
| DQ, lineage, metadata | `samples/dq_*`, audit columns in glue sample |
| Regulatory compliance | Governance sections in case + real-world issues |
| Mentor junior DE | STAR in `prep/interview/`; code review mentions in README pitch |
| Partner BA/DS/EA | Workshop notes in MSB case |

---

## Mandatory skills ↔ samples

| Skill | Proof |
|-------|-------|
| S3, Glue, Lake Formation, Redshift | Architecture doc + samples |
| IAM, VPC, IaC | `docs/03-to-be-architecture.md` § Security |
| Oracle PL/SQL extract | `oracle_extract_customer.sql` |
| Spark | Glue Python sample |
| Airflow | `airflow_hybrid_etl_dag.py` |
| SQL | `dim_customer_scd2.sql`, `dq_income_completeness.sql` |
| Python | `dq_contract.py`, `glue_*`, `kafka_*` |
| Bronze/Silver/Gold | README + to-be architecture |
| Dimensional modeling | SCD2, dim_customer design |

---

## Preferred skills

| Preferred | Repo |
|-----------|------|
| CI/CD | Mention CodePipeline in to-be; extend with `.gitlab-ci.yml` if needed |
| Kinesis/MSK streaming | `samples/kafka_payment_landing.py`, TCB case |
| Tableau/PBI | BI incident section in `05-real-world-issues.md` |
| AWS certification | Add to CV — not in repo |

---

## Application checklist (from JD)

- [ ] Resume highlights BFSI + AWS + Oracle — use README pitch + cases  
- [ ] Notice period & availability  
- [ ] Link this repo (GitHub) as portfolio case study  
- [ ] Quantify MSB/TCB outcomes in CV  

---

## Cover letter bullet (English)

```text
I have six years in data engineering across Vietnamese retail banking programs,
including BCG-led AWS migration at MSB and Techcombank's hybrid streaming layer
for digital banking (~1–2M daily payment checks). I design medallion lakehouses
on S3/Glue/Redshift with Oracle hybrid extract, customer SSOT, and shift-left DQ —
directly aligned with your Data Enhancement scope.
```
