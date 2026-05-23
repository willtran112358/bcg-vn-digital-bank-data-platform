"""
MSK / Kafka consumer → S3 bronze landing (TCB-style payment checks).
Local demo uses in-memory messages; on AWS use confluent-kafka + boto3.
"""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable

PIPELINE_RUN_ID = str(uuid.uuid4())


@dataclass
class PaymentCheckEvent:
    check_id: str
    customer_id: str
    account_id: str
    amount: float
    currency: str
    channel: str
    event_ts: str
    source_system: str = "PAYMENT_SWITCH"

    def to_bronze_record(self) -> dict:
        return {
            **asdict(self),
            "ingest_ts": datetime.now(timezone.utc).isoformat(),
            "pipeline_run_id": PIPELINE_RUN_ID,
        }


def validate_event(raw: dict) -> PaymentCheckEvent | None:
    try:
        if not raw.get("check_id") or raw.get("amount") is None:
            return None
        return PaymentCheckEvent(
            check_id=str(raw["check_id"]),
            customer_id=str(raw.get("customer_id", "")),
            account_id=str(raw.get("account_id", "")),
            amount=float(raw["amount"]),
            currency=str(raw.get("currency", "VND")),
            channel=str(raw.get("channel", "DIGITAL")),
            event_ts=str(raw.get("event_ts", datetime.now(timezone.utc).isoformat())),
        )
    except (TypeError, ValueError):
        return None


def partition_path(event_ts: str, business_tz: str = "Asia/Ho_Chi_Minh") -> str:
    # Production: convert to business date in VN TZ
    day = event_ts[:10] if len(event_ts) >= 10 else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"s3://bank-lake/bronze/payment_checks/dt={day}/"


def landing_records(events: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    ok, dlq = [], []
    for raw in events:
        ev = validate_event(raw)
        if ev:
            ok.append(ev.to_bronze_record())
        else:
            dlq.append(raw)
    return ok, dlq


def simulate_daily_reconciliation(bronze_count: int, core_eod_count: int) -> dict:
    variance = abs(bronze_count - core_eod_count)
    tolerance = max(100, int(0.001 * core_eod_count))
    return {
        "bronze_count": bronze_count,
        "core_eod_count": core_eod_count,
        "variance": variance,
        "within_tolerance": variance <= tolerance,
    }


SAMPLE_STREAM = [
    {"check_id": "CHK001", "customer_id": "C1", "account_id": "A1", "amount": 150000, "channel": "MOBILE"},
    {"check_id": "CHK002", "customer_id": "C2", "account_id": "A2", "amount": 50000, "event_ts": "2025-05-21T08:00:00Z"},
    {"check_id": "", "amount": 1},  # poison → DLQ
]


if __name__ == "__main__":
    ok, dlq = landing_records(SAMPLE_STREAM)
    print(f"pipeline_run_id={PIPELINE_RUN_ID} bronze={len(ok)} dlq={len(dlq)}")
    print("sample_path:", partition_path("2025-05-21T08:00:00Z"))
    print("recon:", simulate_daily_reconciliation(len(ok), 1_850_000))
