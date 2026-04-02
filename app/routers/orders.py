from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from .. import schemas, crud, payment
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/create", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: Optional[schemas.User] = Depends(get_current_user)
):
    try:
        db_order = crud.create_order(db, order, current_user.id if current_user else None)
        return db_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_orders(db, skip=skip, limit=limit, user_id=current_user.id)

@router.get("/{transaction_id}", response_model=schemas.OrderResponse)
def get_order(transaction_id: str, db: Session = Depends(get_db)):
    order = crud.get_order_by_transaction(db, transaction_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{transaction_id}/initiate-payment")
async def initiate_payment(transaction_id: str, db: Session = Depends(get_db)):
    order = crud.get_order_by_transaction(db, transaction_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get frontend URL from environment or use default
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    success_url = f"{frontend_url}/order-success?transaction_id={transaction_id}"
    
    # Generate payment URL
    payment_url = payment.generate_payment_url(
        transaction_id=transaction_id,
        amount=order.total_amount,
        success_url=success_url,
        remark=f"Order {transaction_id}"
    )
    
    return {
        "payment_url": payment_url,
        "transaction_id": transaction_id,
        "amount": order.total_amount
    }

@router.get("/payment/success")
async def payment_success(
    transaction_id: str = Query(...),
    success_hash: str = Query(None),
    success_time: str = Query(None),
    success_amount: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Handle payment success redirect from KHQR
    Customer is redirected here after successful payment
    """
    order = crud.get_order_by_transaction(db, transaction_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify the success signature if provided
    if success_hash and success_time and success_amount:
        if payment.verify_webhook_signature(success_time, transaction_id, success_amount, success_hash):
            # Update order status
            if order.payment_status != "paid":
                crud.update_order(db, order.id, schemas.OrderUpdate(
                    payment_status="paid",
                    status="processing"
                ))
                print(f"Order {transaction_id} payment confirmed via success redirect")
    
    return {
        "status": "success",
        "message": "Payment processed successfully",
        "order_id": transaction_id
    }

@router.post("/payment/callback")
async def payment_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle KHQR payment callback/webhook
    This endpoint receives POST requests from KHQR after payment
    """
    try:
        # Get callback data
        callback_data = await request.json()
        print(f"Payment callback received: {callback_data}")
        
        # Extract data
        transaction_id = callback_data.get("transaction_id")
        amount = callback_data.get("amount")
        status = callback_data.get("status")
        req_time = callback_data.get("req_time")
        signature = callback_data.get("hash")
        
        if not transaction_id:
            return {"status": "error", "message": "No transaction_id provided"}
        
        # Verify webhook signature
        if signature and req_time and amount:
            is_valid = payment.verify_webhook_signature(req_time, transaction_id, amount, signature)
            if not is_valid:
                print(f"Invalid signature for transaction {transaction_id}")
                return {"status": "error", "message": "Invalid signature"}
        else:
            # If no signature, verify via API
            verification = await payment.verify_payment(transaction_id)
            if not payment.is_payment_successful(verification):
                return {"status": "pending", "message": "Payment not confirmed"}
        
        # Update order status
        order = crud.get_order_by_transaction(db, transaction_id)
        if order and order.payment_status != "paid":
            crud.update_order(db, order.id, schemas.OrderUpdate(
                payment_status="paid",
                status="processing"
            ))
            print(f"Order {transaction_id} payment confirmed via webhook")
            return {"status": "success", "message": "Payment confirmed"}
        
        return {"status": "pending", "message": "Order already processed"}
        
    except Exception as e:
        print(f"Payment callback error: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/payment/verify/{transaction_id}")
async def verify_payment_status(transaction_id: str, db: Session = Depends(get_db)):
    """Check payment status for an order"""
    order = crud.get_order_by_transaction(db, transaction_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Verify with KHQR
    verification = await payment.verify_payment(transaction_id)
    
    if payment.is_payment_successful(verification):
        # Update order status if not already updated
        if order.payment_status != "paid":
            crud.update_order(db, order.id, schemas.OrderUpdate(
                payment_status="paid",
                status="processing"
            ))
        
        return {
            "status": "paid",
            "order": order,
            "verification": verification
        }
    
    return {
        "status": order.payment_status,
        "order": order
    }