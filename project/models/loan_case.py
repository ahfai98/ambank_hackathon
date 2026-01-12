from pydantic import BaseModel
from typing import Optional


class LoanCase(BaseModel):
    case_id: str
    monthly_income: float
    monthly_commitments: float
    dsr: float
    employment_type: str
    is_high_networth: bool = False
    relationship_years: Optional[int] = None
