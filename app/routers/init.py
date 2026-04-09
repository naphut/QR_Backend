from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud
from app.database import get_db
import json

router = APIRouter(prefix="/api/init", tags=["initialization"])

@router.post("/setup")
def setup_database(db: Session = Depends(get_db)):
    """
    Temporary endpoint to initialize database with sample data
    This should be removed or secured in production
    """
    try:
        # Create admin user if not exists
        admin_user = db.query(models.User).filter(models.User.email == "admin@store.com").first()
        if not admin_user:
            from app.auth import get_password_hash
            admin_user = models.User(
                email="admin@store.com",
                name="Store Admin",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
        
        # Add sample products if none exist
        existing_products = db.query(models.Product).count()
        if existing_products == 0:
            products = [
                {
                    "code": "TSHIRT001",
                    "name": "Classic T-Shirt",
                    "description": "Comfortable cotton t-shirt perfect for everyday wear",
                    "price": 19.99,
                    "original_price": 29.99,
                    "category": "T-Shirts",
                    "color": "Black",
                    "sizes": json.dumps(["S", "M", "L", "XL"]),
                    "images": json.dumps(["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"]),
                    "stock": 100,
                    "is_active": True
                },
                {
                    "code": "JEANS001",
                    "name": "Slim Fit Jeans",
                    "description": "Modern slim fit denim jeans with stretch comfort",
                    "price": 49.99,
                    "original_price": 69.99,
                    "category": "Pants",
                    "color": "Blue",
                    "sizes": json.dumps(["30", "32", "34", "36"]),
                    "images": json.dumps(["https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"]),
                    "stock": 50,
                    "is_active": True
                },
                {
                    "code": "HOODIE001",
                    "name": "Cozy Hoodie",
                    "description": "Warm and comfortable hoodie for casual days",
                    "price": 35.99,
                    "original_price": 49.99,
                    "category": "Sweatshirts",
                    "color": "Gray",
                    "sizes": json.dumps(["S", "M", "L", "XL"]),
                    "images": json.dumps(["https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400"]),
                    "stock": 30,
                    "is_active": True
                }
            ]
            
            for product_data in products:
                product = models.Product(**product_data)
                db.add(product)
        
        db.commit()
        
        return {
            "message": "Database initialized successfully",
            "admin_user": admin_user.email,
            "products_count": len(products) if existing_products == 0 else existing_products
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize database: {str(e)}"
        )
