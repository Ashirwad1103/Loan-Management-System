from pydantic import BaseModel
from typing import Optional
from ..enums.loan_applicaton import EmploymentStatusEnum

class LoanApplicationBase(BaseModel):
    name: str
    credit_score: float
    loan_amount: float
    loan_purpose: str
    income: float
    employment_status: EmploymentStatusEnum
    debt_to_income_ratio: float

class LoanApplicationCreate(LoanApplicationBase):
    pass

class LoanApplicationUpdate(BaseModel):
    uuid: str
    name: Optional[str] = None
    credit_score: Optional[float] = None
    loan_amount: Optional[float] = None
    loan_purpose: Optional[str] = None
    income: Optional[float] = None
    employment_status: Optional[EmploymentStatusEnum] = None
    debt_to_income_ratio: Optional[float] = None

class LoanApplication(LoanApplicationBase):
    uuid: str
    risk_score: float
    status: str

    class Config:
        orm_mode = True


