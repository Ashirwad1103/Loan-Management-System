from sqlalchemy.orm import Session
from . import model, schemas


def create_loan_application(uuid: str, risk_score: float, status: str, loan_application: schemas.LoanApplicationCreate, db: Session):
    db_loan_application = model.LoanApplications(    
        uuid = uuid,
        name = loan_application.name,
        credit_score = loan_application.credit_score,
        loan_amount =  loan_application.loan_amount,
        loan_purpose = loan_application.loan_purpose,
        income =  loan_application.income,
        employment_status =  loan_application.employment_status,
        debt_to_income_ratio = loan_application.debt_to_income_ratio,
        risk_score = risk_score, 
        status = status
    )

    db.add(db_loan_application)
    db.commit()
    db.refresh(db_loan_application)
    return db_loan_application


def get_loan_application(uuid: str, db: Session):
    db_loan_application = db.query(model.LoanApplications).filter(model.LoanApplications.uuid==uuid).first()
    return db_loan_application

def update_loan_application(loan_application: model.LoanApplications, db: Session):
    db.add(loan_application)
    db.commit()
    db.refresh(loan_application)
    return loan_application


def delete_loan_application(uuid: str, db: Session):
    db_loan_application = get_loan_application(uuid=uuid, db=db)
    db.delete(db_loan_application)
    db.commit()