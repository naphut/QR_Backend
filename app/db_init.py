"""
Automatic database initialization for QR E-commerce
This script runs on startup to ensure database has required data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import json

def initialize_database():
    """Initialize database with admin user and sample products"""
    print("🔄 Initializing database...")
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Always ensure admin user exists
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
            print("✅ Created admin user")
        else:
            # Ensure admin has correct privileges
            if not admin_user.is_admin:
                admin_user.is_admin = True
                print("✅ Updated admin user privileges")
        
        # Ensure sample products exist
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
            
            print(f"✅ Added {len(products)} sample products")
        else:
            print(f"✅ Found {existing_products} existing products")
        
        db.commit()
        print("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()
