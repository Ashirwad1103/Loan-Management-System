from fastapi import APIRouter
from .endpoint import loan_application_router

router = APIRouter(
    prefix="/api",
    tags=["api"], 
    responses={404: {"description": "Not found"}}
)


router.include_router(loan_application_router)