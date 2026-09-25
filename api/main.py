import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FreemannPay | Payment Simulation API")

payments_store = {}

class PaymentPayload(BaseModel):
    user_id: int
    amount: float
    currency: str
    method: str  # CREDIT_CARD, PIX, or BOLETO

@app.post("/payments", status_code=201)
def create_payment(payment: PaymentPayload):
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    payment_id = str(uuid.uuid4())
    new_payment = {
        "id": payment_id,
        "user_id": payment.user_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "method": payment.method,
        "status": "PENDING"
    }
    payments_store[payment_id] = new_payment
    return new_payment

@app.get("/payments/{payment_id}")
def get_payment(payment_id: str):
    if payment_id not in payments_store:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payments_store[payment_id]