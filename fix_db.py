#!/usr/bin/env python3
"""
Database initialization script for QR E-commerce
This script creates initial admin user and sample products
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import json

def create_sample_data():
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(models.User).filter(models.User.email == "admin@store.com").first()
        if not admin_user:
            # Create admin user
            admin_user = models.User(
                email="admin@store.com",
                name="Store Admin",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LrUpm",  # "admin123"
                is_admin=True
            )
            db.add(admin_user)
            print("✅ Created admin user: admin@store.com")
        else:
            # Update existing user to be admin
            admin_user.is_admin = True
            print("✅ Updated admin user privileges")
        
        # Check if products exist
        existing_products = db.query(models.Product).count()
        if existing_products == 0:
            # Create sample products
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
                print(f"✅ Added product: {product_data['name']}")
        else:
            print(f"✅ Products already exist: {existing_products} products")
        
        db.commit()
        print("\n🎉 Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
