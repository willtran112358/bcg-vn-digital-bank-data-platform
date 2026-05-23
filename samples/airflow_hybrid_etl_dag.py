"""
Airflow DAG sketch: hybrid Oracle → S3 → Glue → Redshift (nightly customer SSOT).
Requires: airflow, providers-amazon, providers-oracle (not installed in minimal requirements).
"""
from __future__ import annotations

from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import BranchPythonOperator, PythonOperator
    from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
    from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
except ImportError:
    DAG = None  # type: ignore

default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "email_on_failure": True,
}

BUSINESS_DATE = "{{ ds }}"
S3_MARKER = f"s3://bank-landing/oracle/customer/dt={BUSINESS_DATE}/_SUCCESS"
GLUE_JOB = "customer_bronze_to_silver"
REDSHIFT_CONN = "redshift_prod"


def check_dq_and_branch(**context) -> str:
    """Call dq_contract logic or Redshift DQ query; return task_id to branch."""
    # block_publish = run_dq_on_silver_partition(BUSINESS_DATE)
    block_publish = False
    return "skip_gold_publish" if block_publish else "redshift_merge_scd2"


if DAG is not None:
    with DAG(
        dag_id="hybrid_customer_etl_nightly",
        default_args=default_args,
        schedule="0 2 * * *",  # 02:00 UTC ~ 09:00 VN — adjust per extract window
        start_date=datetime(2025, 1, 1),
        catchup=False,
        tags=["banking", "customer", "hybrid"],
    ) as dag:
        start = EmptyOperator(task_id="start")

        wait_landing = S3KeySensor(
            task_id="wait_oracle_unload_success",
            bucket_key=S3_MARKER.replace("s3://", "").split("/", 1)[1],
            bucket_name="bank-landing",
            timeout=60 * 60 * 4,
        )

        glue_silver = GlueJobOperator(
            task_id="glue_bronze_to_silver",
            job_name=GLUE_JOB,
            script_args={"--business_date": BUSINESS_DATE},
            wait_for_completion=True,
        )

        dq_branch = BranchPythonOperator(
            task_id="dq_gate",
            python_callable=check_dq_and_branch,
        )

        redshift_merge = EmptyOperator(task_id="redshift_merge_scd2")  # replace with SQL operator
        skip_publish = EmptyOperator(task_id="skip_gold_publish")

        end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

        start >> wait_landing >> glue_silver >> dq_branch
        dq_branch >> [redshift_merge, skip_publish] >> end

else:
    # Print structure when Airflow not installed
    print("Airflow not installed — DAG definition is documentation-only.")
    print("Flow: wait S3 _SUCCESS → Glue silver → DQ branch → Redshift SCD2 or skip")
