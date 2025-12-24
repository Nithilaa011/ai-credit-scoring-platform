from fastapi import APIRouter
from pydantic import BaseModel
from app.services.credit_model import predict_credit_score

router = APIRouter(prefix="/credit", tags=["Credit Scoring"])

class CreditInput(BaseModel):
    monthly_income: float
    avg_upi_transactions: int
    bill_payment_ratio: float
    income_consistency: float

@router.post("/score")
def calculate_credit_score(data: CreditInput):
    return predict_credit_score(data.dict())
