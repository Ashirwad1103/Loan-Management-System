from fastapi import APIRouter, Depends, HTTPException, status
from ..db import schemas, session, crud
from uuid import uuid4
from sqlalchemy.orm import Session
from ..queue import producer
from ..services import risk_assessment, loan_approval
from ..loggers.loan_application_logger import loan_application_logger

loan_application_router = APIRouter(
    prefix="/loan_application"
) 


@loan_application_router.post("/applications", status_code=status.HTTP_201_CREATED, response_description="Loan application created successfully")
def apply_loan(loan_application: schemas.LoanApplicationCreate):
    try: 
        uuid = str(uuid4())
        loan_application_dict = loan_application.dict()
        loan_application_dict['uuid'] = uuid
        producer.send_to_queue(application_dict=loan_application_dict)
        loan_application_logger.info(msg="Loan application created successfully")
        return {"application_id": uuid}
    except Exception as e: 
        loan_application_logger.exception(msg={e})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

@loan_application_router.get("/applications", response_model=schemas.LoanApplication, status_code=status.HTTP_200_OK, response_description="Loan application info") 
def loan_application_info(uuid: str, db: Session = Depends(session.get_db)):
    try:
        db_loan_application = crud.get_loan_application(uuid=uuid, db=db)
        if db_loan_application is None:
            loan_application_logger.info(msg="Loan application not found")
            raise HTTPException(status_code=404, detail="Loan application not found")
        loan_application_logger.info(msg="Loan application info")
        return db_loan_application
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e: 
        loan_application_logger.exception(msg={e})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@loan_application_router.put("/applications", status_code=status.HTTP_200_OK, response_description="Loan application updated successfully")
def update_loan_application(loan_application: schemas.LoanApplicationUpdate, db: Session = Depends(session.get_db)):
    try: 
        db_loan_application = crud.get_loan_application(uuid=loan_application.uuid, db=db)
        if db_loan_application is None:
            loan_application_logger.info(msg="Loan application not found")
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        if db_loan_application.status == "Approved":
            loan_application_logger.info(msg="Approved applications cannot be updated")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Approved applications cannot be updated")

        def update_field(target, source, field):
            """Update the target field if the source field is not None."""
            setattr(target, field, getattr(target, field) if getattr(source, field) is None else getattr(source, field))

        fields_to_update = [
            'name', 'credit_score', 'loan_amount', 'loan_purpose',
            'income', 'employment_status', 'debt_to_income_ratio'
        ]

        for field in fields_to_update:
            update_field(target=db_loan_application, source=loan_application, field=field)

        db_loan_application.risk_score = risk_assessment.RiskAssessment.assess(loan_application=db_loan_application)
        db_loan_application.status = loan_approval.LoanApproval.approve(risk_score=db_loan_application.risk_score)

        loan_application_logger.info("Loan application updated successfully")
        return crud.update_loan_application(loan_application=db_loan_application, db=db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e: 
        loan_application_logger.exception(msg={e})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


@loan_application_router.delete("/applications", status_code=status.HTTP_204_NO_CONTENT, response_description="Loan application deleted successfully") 
def delete_loan_application(uuid: str, db: Session = Depends(session.get_db)):
    try: 
        db_loan_application = crud.get_loan_application(uuid=uuid, db=db)
        if db_loan_application is None:
            loan_application_logger.info(msg="Loan application not found")
            raise HTTPException(status_code=404, detail="Loan application not found")
        crud.delete_loan_application(uuid=uuid, db=db)
        loan_application_logger.info(msg="Loan application deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e: 
        loan_application_logger.exception(msg={e})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
