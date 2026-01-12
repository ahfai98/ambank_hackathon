from models.loan_case import LoanCase
from models.decision_result import DecisionResult


def evaluate(case: LoanCase) -> DecisionResult:
    approve_flags = []
    reject_flags = []

    if case.dsr > 0.8:
        reject_flags.append("DSR exceeds 80%")

    if case.employment_type == "permanent":
        approve_flags.append("Stable employment")

    if case.is_high_networth:
        approve_flags.append("High net-worth customer")

    conflicts = list(set(approve_flags) & set(reject_flags))

    if approve_flags and reject_flags:
        recommendation = "REVIEW"
    elif reject_flags:
        recommendation = "REJECT"
    else:
        recommendation = "APPROVE"

    return DecisionResult(
        recommendation=recommendation,
        approve_flags=approve_flags,
        reject_flags=reject_flags,
        conflicts=conflicts,
        explanation=""
    )
