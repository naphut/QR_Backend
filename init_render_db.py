#!/usr/bin/env python3
"""
Database initialization script for Render deployment
Run this script after deployment to create database tables and sample data
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to Python path
sys.path.append('/opt/render/project/src')

load_dotenv()

def init_database():
    try:
        from app import models, database
        from app.crud import create_user, create_product
        from app.schemas import UserCreate, ProductCreate
        from sqlalchemy.orm import Session
        
        print("🔄 Starting database initialization...")
        
        # Create database tables
        models.Base.metadata.create_all(bind=database.engine)
        print("✅ Database tables created successfully")
        
        # Create session
        db = SessionLocal()
        
        try:
            # Check if admin user already exists
            from app.crud import get_user_by_email
            existing_admin = get_user_by_email(db, "admin123@gmail.com")
            
            if not existing_admin:
                # Create admin user
                admin_user = UserCreate(
                    email="admin123@gmail.com",
                    password="admin123",
                    name="Admin User",
                    phone="85512345678",
                    address="Phnom Penh, Cambodia"
                )
                create_user(db, admin_user, is_admin=True)
                print("✅ Admin user created: admin123@gmail.com / admin123")
            
            # Check if demo user already exists
            existing_demo = get_user_by_email(db, "demo@routine.com")
            
            if not existing_demo:
                # Create demo user
                demo_user = UserCreate(
                    email="demo@routine.com",
                    password="demo123",
                    name="Demo User",
                    phone="85587654321",
                    address="Phnom Penh, Cambodia"
                )
                create_user(db, demo_user, is_admin=False)
                print("✅ Demo user created: demo@routine.com / demo123")
            
            # Check if products already exist
            from app.crud import get_products
            existing_products = get_products(db, skip=0, limit=1)
            
            if not existing_products:
                # Create sample products
                sample_products = [
                    ProductCreate(
                        code="QR001",
                        name="Classic T-Shirt",
                        description="Comfortable cotton t-shirt with QR code design",
                        price=15.99,
                        original_price=19.99,
                        category="T-Shirts",
                        color="White",
                        sizes='["S", "M", "L", "XL"]',
                        images='["https://via.placeholder.com/300x300?text=T-Shirt"]',
                        stock=100
                    ),
                    ProductCreate(
                        code="QR002",
                        name="QR Hoodie",
                        description="Warm hoodie with unique QR code pattern",
                        price=39.99,
                        original_price=49.99,
                        category="Hoodies",
                        color="Black",
                        sizes='["S", "M", "L", "XL", "XXL"]',
                        images='["https://via.placeholder.com/300x300?text=Hoodie"]',
                        stock=50
                    ),
                    ProductCreate(
                        code="QR003",
                        name="Digital Tank Top",
                        description="Lightweight tank top with digital QR print",
                        price=12.99,
                        original_price=16.99,
                        category="Tank Tops",
                        color="Blue",
                        sizes='["S", "M", "L"]',
                        images='["https://via.placeholder.com/300x300?text=Tank+Top"]',
                        stock=75
                    )
                ]
                
                for product_data in sample_products:
                    create_product(db, product_data)
                
                print("✅ Sample products created (3 items)")
            
            db.commit()
            print("🎉 Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
