"""
Banking customer data quality contract — lightweight Great Expectations-style checks.
Run: python dq_contract.py
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class Severity(str, Enum):
    CRITICAL = "CRITICAL"  # block gold publish
    WARNING = "WARNING"    # ticket only


@dataclass
class CheckResult:
    rule_id: str
    passed: bool
    severity: Severity
    detail: str


@dataclass
class CustomerSilverBatch:
    rows: list[dict[str, Any]]
    business_date: str
    pipeline_run_id: str


def check_customer_id_not_null(batch: CustomerSilverBatch) -> CheckResult:
    nulls = sum(1 for r in batch.rows if not r.get("customer_id"))
    passed = nulls == 0
    return CheckResult(
        rule_id="SILVER_CUSTOMER_ID_NOT_NULL",
        passed=passed,
        severity=Severity.CRITICAL,
        detail=f"null customer_id count={nulls}",
    )


def check_income_non_negative(batch: CustomerSilverBatch) -> CheckResult:
    bad = [
        r["customer_id"]
        for r in batch.rows
        if r.get("declared_income_amount") is not None and float(r["declared_income_amount"]) < 0
    ]
    return CheckResult(
        rule_id="SILVER_INCOME_NON_NEGATIVE",
        passed=len(bad) == 0,
        severity=Severity.CRITICAL,
        detail=f"negative income customers={bad[:5]}",
    )


def check_mobile_app_income_completeness(batch: CustomerSilverBatch, min_pct: float = 0.50) -> CheckResult:
    """Warning if mobile channel fill rate below threshold (pilot SLA)."""
    mobile = [r for r in batch.rows if r.get("onboarding_channel") == "MOBILE_APP"]
    if not mobile:
        return CheckResult("SILVER_MOBILE_INCOME_FILL", True, Severity.WARNING, "no mobile rows")
    filled = sum(1 for r in mobile if r.get("declared_income_amount") is not None)
    pct = filled / len(mobile)
    return CheckResult(
        rule_id="SILVER_MOBILE_INCOME_FILL",
        passed=pct >= min_pct,
        severity=Severity.WARNING,
        detail=f"mobile fill_rate={pct:.1%} threshold={min_pct:.0%}",
    )


def check_no_imputed_in_declared(batch: CustomerSilverBatch) -> CheckResult:
    """Ensure estimated values did not leak into declared column name."""
    leaked = [r["customer_id"] for r in batch.rows if r.get("is_imputed") and r.get("declared_income_amount")]
    return CheckResult(
        rule_id="GOVERNANCE_NO_IMPUTED_IN_DECLARED",
        passed=len(leaked) == 0,
        severity=Severity.CRITICAL,
        detail=f"leaked rows={len(leaked)}",
    )


CHECKS: list[Callable[[CustomerSilverBatch], CheckResult]] = [
    check_customer_id_not_null,
    check_income_non_negative,
    check_mobile_app_income_completeness,
    check_no_imputed_in_declared,
]


def run_dq(batch: CustomerSilverBatch) -> tuple[bool, list[CheckResult]]:
    results = [fn(batch) for fn in CHECKS]
    block = any(not r.passed and r.severity == Severity.CRITICAL for r in results)
    return block, results


if __name__ == "__main__":
    sample = CustomerSilverBatch(
        pipeline_run_id="demo-run-001",
        business_date="2025-05-21",
        rows=[
            {"customer_id": "C1", "onboarding_channel": "MOBILE_APP", "declared_income_amount": None},
            {"customer_id": "C2", "onboarding_channel": "BRANCH", "declared_income_amount": 30000000},
        ],
    )
    blocked, results = run_dq(sample)
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.severity.value} {r.rule_id}: {r.detail}")
    print("BLOCK_GOLD_PUBLISH=" + str(blocked))
