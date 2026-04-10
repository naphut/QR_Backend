from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.payment import generate_payment_url, verify_payment

router = APIRouter(prefix="/api/payment", tags=["payment"])

class PaymentRequest(BaseModel):
    transaction_id: str
    amount: float
    success_url: str
    remark: str = "Payment for order"

class PaymentResponse(BaseModel):
    payment_url: str
    transaction_id: str

@router.post("/generate", response_model=PaymentResponse)
def create_payment_url(request: PaymentRequest):
    """
    Generate KHQR payment URL
    """
    try:
        payment_url = generate_payment_url(
            transaction_id=request.transaction_id,
            amount=request.amount,
            success_url=request.success_url,
            remark=request.remark
        )
        
        return PaymentResponse(
            payment_url=payment_url,
            transaction_id=request.transaction_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate payment URL: {str(e)}"
        )

@router.post("/verify")
async def verify_payment_status(transaction_id: str):
    """
    Verify payment status with KHQR API
    """
    try:
        result = await verify_payment(transaction_id)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to verify payment: {str(e)}"
        )
