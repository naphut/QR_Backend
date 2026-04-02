from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc, func
from . import models, schemas
import json
import time
import random
import string

def generate_transaction_id():
    """Generate unique transaction ID with timestamp and random string"""
    timestamp = str(int(time.time() * 1000))  # Use milliseconds for better uniqueness
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"ORD_{timestamp}_{random_str}"

def create_user(db: Session, user: schemas.UserCreate):
    from .auth import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        phone=user.phone,
        address=user.address,
        is_admin=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: dict):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        for key, value in user_update.items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    category: str = None,
    search: str = None,
    min_price: float = None,
    max_price: float = None,
    color: str = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    """Enhanced product query with filtering and sorting"""
    query = db.query(models.Product).filter(models.Product.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(models.Product.category == category)
    
    if search:
        search_filter = or_(
            models.Product.name.ilike(f"%{search}%"),
            models.Product.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    if color:
        query = query.filter(models.Product.color.ilike(f"%{color}%"))
    
    # Apply sorting
    sort_column = getattr(models.Product, sort_by, models.Product.created_at)
    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    # Apply pagination
    return query.offset(skip).limit(limit).all()

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_categories(db: Session):
    """Get all unique product categories"""
    result = db.query(models.Product.category).filter(models.Product.is_active == True).distinct().all()
    return [row[0] for row in result]

def get_colors(db: Session):
    """Get all unique product colors"""
    result = db.query(models.Product.color).filter(models.Product.is_active == True).distinct().all()
    return [row[0] for row in result]

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def create_order(db: Session, order: schemas.OrderCreate, user_id: int = None):
    max_retries = 3
    transaction_id = None
    
    for attempt in range(max_retries):
        transaction_id = generate_transaction_id()
        # Check if transaction ID already exists
        existing = db.query(models.Order).filter(models.Order.transaction_id == transaction_id).first()
        if not existing:
            break
        if attempt == max_retries - 1:
            raise Exception("Failed to generate unique transaction ID")
    
    # Calculate total amount and prepare order items
    total = 0
    order_items_data = []
    
    for item in order.items:
        product = get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")
        
        item_total = product.price * item.quantity
        total += item_total
        order_items_data.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "product_code": product.code,
            "quantity": item.quantity,
            "price": product.price,
            "size": item.size,
            "color": item.color
        })
        
        # Update stock
        product.stock -= item.quantity
    
    db_order = models.Order(
        transaction_id=transaction_id,
        user_id=user_id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        total_amount=total,
        status="pending",
        payment_status="pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item_data in order_items_data:
        db_item = models.OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(models.Order).order_by(models.Order.created_at.desc())
    if user_id:
        query = query.filter(models.Order.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_order_by_transaction(db: Session, transaction_id: str):
    return db.query(models.Order).filter(models.Order.transaction_id == transaction_id).first()

def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate):
    db_order = get_order_by_id(db, order_id)
    if db_order:
        update_data = order_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def get_all_users(db: Session):
    return db.query(models.User).all()

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user and not db_user.is_admin:
        db.delete(db_user)
        db.commit()
    return db_user