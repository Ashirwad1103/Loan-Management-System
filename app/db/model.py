from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .session import Base

class LoanApplications(Base):
    __tablename__ = 'loan_applications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, index=True)
    name = Column(String)
    credit_score = Column(Float)
    loan_amount =  Column(Float)
    loan_purpose = Column(String)
    income =  Column(Float)
    employment_status =  Column(String)
    debt_to_income_ratio = Column(Float)
    risk_score = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    def __repr__(self):
        return  (f"<LoanApplications(id={self.id}, name={self.name}, credit_score={self.credit_score}, "
                f"loan_amount={self.loan_amount}, loan_purpose={self.loan_purpose}, income={self.income}, "
                f"employment_status={self.employment_status}, debt_to_income_ratio={self.debt_to_income_ratio})>")
