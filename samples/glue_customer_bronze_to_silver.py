"""
Glue-style Spark job: bronze → silver customer conformation.
Run locally in DRY_RUN=1 mode without Spark cluster.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

PIPELINE_RUN_ID = os.environ.get("PIPELINE_RUN_ID", str(uuid.uuid4()))
DRY_RUN = os.environ.get("DRY_RUN", "1") == "1"
BUSINESS_DATE = os.environ.get("BUSINESS_DATE", "2025-05-21")


def normalize_name(name: str | None) -> str:
    if not name:
        return ""
    # Production: Unicode NFKD + strip diacritics for join key only
    return name.strip().lower()


def record_hash(row: dict[str, Any]) -> str:
    payload = json.dumps(row, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


def bronze_to_silver_customer(bronze_row: dict[str, Any]) -> dict[str, Any] | None:
    """Map raw Oracle extract to silver contract. Returns None if quarantine."""
    cid = bronze_row.get("customer_id")
    if not cid:
        return None

    income = bronze_row.get("declared_income_amount")
    if income is not None and float(income) < 0:
        return None  # quarantine — invalid amount

    silver = {
        "customer_id": str(cid),
        "cif_number": bronze_row.get("cif_number"),
        "full_name": bronze_row.get("full_name"),
        "search_name": normalize_name(bronze_row.get("full_name")),
        "national_id": bronze_row.get("national_id"),
        "phone_mobile": bronze_row.get("phone_mobile"),
        "declared_income_amount": income,
        "declared_income_currency": bronze_row.get("income_currency") or "VND",
        "onboarding_channel": bronze_row.get("onboarding_channel"),
        "branch_code": bronze_row.get("branch_code"),
        "customer_status": bronze_row.get("customer_status"),
        "source_system": bronze_row.get("source_system", "ORACLE_CORE"),
        "source_last_update_ts": bronze_row.get("last_update_ts"),
        "business_date": BUSINESS_DATE,
        "ingest_ts": datetime.now(timezone.utc).isoformat(),
        "pipeline_run_id": PIPELINE_RUN_ID,
        "record_hash": record_hash(bronze_row),
    }
    return silver


# --- Glue entrypoint sketch (when DRY_RUN=0 on AWS) ---
def glue_main():
    """
    from awsglue.context import GlueContext
    from pyspark.context import SparkContext

    sc = SparkContext()
    glue = GlueContext(sc)
    spark = glue.spark_session
    dyf = glue.create_dynamic_frame.from_catalog(database="bronze", table_name="customer")
    # map bronze_to_silver_customer via UDF; write parquet to s3://.../silver/customer/
    """
    raise NotImplementedError("Deploy on AWS Glue with catalog tables configured")


SAMPLE_BRONZE = [
    {
        "customer_id": "C001",
        "cif_number": "CIF99001",
        "full_name": "Nguyễn Văn A",
        "national_id": "001234567890",
        "declared_income_amount": 25000000,
        "income_currency": "VND",
        "onboarding_channel": "BRANCH",
        "branch_code": "HN001",
        "customer_status": "ACTIVE",
        "last_update_ts": "2025-05-20T10:00:00",
        "source_system": "ORACLE_CORE",
    },
    {
        "customer_id": "C002",
        "full_name": "Tran Thi B",
        "declared_income_amount": None,
        "onboarding_channel": "MOBILE_APP",
        "customer_status": "ACTIVE",
        "last_update_ts": "2025-05-20T11:00:00",
        "source_system": "ORACLE_CORE",
    },
]


if __name__ == "__main__":
    results = []
    quarantine = []
    for raw in SAMPLE_BRONZE:
        out = bronze_to_silver_customer(raw)
        if out:
            results.append(out)
        else:
            quarantine.append(raw)
    print(f"pipeline_run_id={PIPELINE_RUN_ID} silver={len(results)} quarantine={len(quarantine)}")
    for r in results:
        print(json.dumps(r, ensure_ascii=True))
