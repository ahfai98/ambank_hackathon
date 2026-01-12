from pydantic import BaseModel
from typing import List


class DecisionResult(BaseModel):
    recommendation: str  # APPROVE / REJECT / REVIEW
    approve_flags: List[str]
    reject_flags: List[str]
    conflicts: List[str]
    explanation: str
