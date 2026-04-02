from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import schemas, crud, auth, models
from ..database import get_db

router = APIRouter()

@router.post("/products", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    # Check if product code already exists
    existing_product = db.query(models.Product).filter(models.Product.code == product.code).first()
    if existing_product:
        raise HTTPException(
            status_code=400, 
            detail=f"Product with code '{product.code}' already exists. Please use a unique product code."
        )
    
    try:
        return crud.create_product(db, product)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create product: {str(e)}"
        )

@router.get("/products", response_model=List[schemas.Product])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    return crud.get_all_products(db, skip=skip, limit=limit)

@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(
    product_id: int,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    # Check if product exists
    existing_product = crud.get_product(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if new code conflicts with another product
    if product_update.code and product_update.code != existing_product.code:
        code_conflict = db.query(models.Product).filter(
            models.Product.code == product_update.code,
            models.Product.id != product_id
        ).first()
        if code_conflict:
            raise HTTPException(
                status_code=400,
                detail=f"Product with code '{product_update.code}' already exists. Please use a unique product code."
            )
    
    try:
        product = crud.update_product(db, product_id, product_update)
        return product
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update product: {str(e)}"
        )

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.get("/orders", response_model=List[schemas.OrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(models.Order)
    if status:
        query = query.filter(models.Order.status == status)
    return query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()

@router.put("/orders/{order_id}")
def update_order_status(
    order_id: int,
    order_update: schemas.OrderUpdate,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    order = crud.update_order(db, order_id, order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/users", response_model=List[schemas.User])
def get_all_users(
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    return crud.get_all_users(db)

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/stats")
def get_stats(
    current_user: schemas.User = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    total_orders = db.query(func.count(models.Order.id)).scalar() or 0
    total_products = db.query(func.count(models.Product.id)).scalar() or 0
    total_users = db.query(func.count(models.User.id)).scalar() or 0
    total_revenue = db.query(func.sum(models.Order.total_amount)).filter(
        models.Order.payment_status == "paid"
    ).scalar() or 0
    
    # Get last 6 months revenue data
    from datetime import datetime, timedelta
    import calendar
    
    revenue_data = []
    orders_data = []
    months = []
    
    for i in range(5, -1, -1):
        date = datetime.now() - timedelta(days=30*i)
        month_name = calendar.month_abbr[date.month]
        months.append(month_name)
        
        # Get revenue for that month
        start_date = datetime(date.year, date.month, 1)
        if date.month == 12:
            end_date = datetime(date.year + 1, 1, 1)
        else:
            end_date = datetime(date.year, date.month + 1, 1)
        
        monthly_revenue = db.query(func.sum(models.Order.total_amount)).filter(
            models.Order.payment_status == "paid",
            models.Order.created_at >= start_date,
            models.Order.created_at < end_date
        ).scalar() or 0
        
        monthly_orders = db.query(func.count(models.Order.id)).filter(
            models.Order.created_at >= start_date,
            models.Order.created_at < end_date
        ).scalar() or 0
        
        revenue_data.append(float(monthly_revenue))
        orders_data.append(monthly_orders)
    
    return {
        "totalOrders": total_orders,
        "totalProducts": total_products,
        "totalUsers": total_users,
        "totalRevenue": float(total_revenue),
        "revenueData": {
            "labels": months,
            "values": revenue_data
        },
        "ordersData": {
            "labels": months,
            "values": orders_data
        }
    }