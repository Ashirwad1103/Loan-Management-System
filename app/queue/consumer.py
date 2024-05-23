import pika
import json
from ..services.risk_assessment import RiskAssessment
from app.services.loan_approval import LoanApproval
from ..db import crud, schemas, session
from fastapi import Depends
import os

def process_application(uuid: str, loan_application: schemas.LoanApplicationCreate):
    risk_score = RiskAssessment.assess(loan_application=loan_application)
    status = LoanApproval.approve(risk_score)
    db = session.SessionLocal()
    crud.create_loan_application(uuid=uuid, risk_score=risk_score, status=status, loan_application=loan_application, db=db)
    print(f"Worker: Application ID: {uuid} Status: {status}")

def callback(ch, method, properties, body):
    application_dict = json.loads(body)
    loan_application = schemas.LoanApplicationCreate(
        name = application_dict['name'],
        credit_score=application_dict['credit_score'],
        loan_amount=application_dict['loan_amount'],
        loan_purpose=application_dict['loan_purpose'],
        income=application_dict['income'],
        employment_status=application_dict['employment_status'],
        debt_to_income_ratio=application_dict['debt_to_income_ratio']
    )
    process_application(uuid=application_dict['uuid'], loan_application=loan_application)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='loan_applications')
    channel.basic_consume(queue='loan_applications', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
 
