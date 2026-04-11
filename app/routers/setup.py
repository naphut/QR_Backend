from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
import json

router = APIRouter()

@router.post("/setup-platform")
def setup_platform(db: Session = Depends(get_db)):
    """Public endpoint to initialize the platform with admin user and products"""
    try:
        # Create admin user
        admin_email = "admin@qrshop.com"
        existing_admin = crud.get_user_by_email(db, admin_email)
        
        if not existing_admin:
            admin_user = schemas.UserCreate(
                email=admin_email,
                password="admin123",
                name="QR Shop Admin",
                is_admin=True
            )
            # Manually set admin flag since create_user might not work properly
            from ..auth import get_password_hash
            hashed_password = get_password_hash(admin_user.password)
            from .. import models
            db_admin = models.User(
                email=admin_user.email,
                hashed_password=hashed_password,
                name=admin_user.name,
                is_admin=True  # Force admin flag
            )
            db.add(db_admin)
            db.commit()
            db.refresh(db_admin)
            print("✅ Admin user created with admin privileges")
        else:
            # Force update existing user to admin
            from .. import models
            db_admin = db.query(models.User).filter(models.User.email == admin_email).first()
            if db_admin:
                db_admin.is_admin = True
                db.commit()
                print("✅ Existing user updated to admin")
        
        # Add sample products
        products_count = len(crud.get_all_products(db, skip=0, limit=100))
        
        if products_count == 0:
            sample_products = [
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
                },
                {
                    "code": "DRESS001",
                    "name": "Summer Dress",
                    "description": "Elegant summer dress perfect for special occasions",
                    "price": 59.99,
                    "original_price": 89.99,
                    "category": "Dresses",
                    "color": "Pink",
                    "sizes": json.dumps(["XS", "S", "M", "L"]),
                    "images": json.dumps(["https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400"]),
                    "stock": 25,
                    "is_active": True
                },
                {
                    "code": "JACKET001",
                    "name": "Denim Jacket",
                    "description": "Classic denim jacket with modern fit",
                    "price": 45.99,
                    "original_price": 65.99,
                    "category": "Jackets",
                    "color": "Blue",
                    "sizes": json.dumps(["S", "M", "L", "XL"]),
                    "images": json.dumps(["https://images.unsplash.com/photo-1548126093-3b3a4f5c6f3f?w=400"]),
                    "stock": 40,
                    "is_active": True
                }
            ]
            
            for product_data in sample_products:
                product = schemas.ProductCreate(**product_data)
                crud.create_product(db, product)
            
            print("✅ Sample products created")
        
        # Verify setup
        final_products = crud.get_all_products(db, skip=0, limit=100)
        admin_check = crud.get_user_by_email(db, admin_email)
        
        return {
            "status": "success",
            "message": "Platform setup completed successfully",
            "admin_user": {
                "email": admin_email,
                "password": "admin123",
                "is_admin": admin_check.is_admin if admin_check else False
            },
            "products_count": len(final_products),
            "platform_ready": len(final_products) > 0 and (admin_check.is_admin if admin_check else False)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Platform setup failed: {str(e)}"
        )
