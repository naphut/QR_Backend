from app.database import SessionLocal, engine
from app import models
from app.auth import get_password_hash
import json
import os

def init_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_email = "admin123@gmail.com"
        admin = db.query(models.User).filter(models.User.email == admin_email).first()
        
        if not admin:
            admin = models.User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                name="Admin User",
                phone="1234567890",
                address="Admin Address",
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created")
            print("   Email: admin123@gmail.com")
            print("   Password: admin123")
        
        # Create demo user for testing
        demo_email = "demo@routine.com"
        demo = db.query(models.User).filter(models.User.email == demo_email).first()
        
        if not demo:
            demo_user = models.User(
                email=demo_email,
                hashed_password=get_password_hash("demo123"),
                name="Demo User",
                phone="1234567890",
                address="Demo Address",
                is_admin=False
            )
            db.add(demo_user)
            db.commit()
            print("✅ Demo user created")
            print("   Email: demo@routine.com")
            print("   Password: demo123")
        
        # Create sample products if none exist
        if db.query(models.Product).count() == 0:
            sample_products = [
                models.Product(
                    code="TS001",
                    name="Regular Fit T-Shirt",
                    description="The Men's Short-Sleeve Fitted T-shirt is the perfect choice for those who love a neat, dynamic style. With a basic yet sophisticated design, the shirt is easily combined with various outfits, suitable for both work and casual outings.",
                    price=8.95,
                    original_price=13.59,
                    category="T-Shirts",
                    color="Green",
                    sizes=json.dumps(["S", "M", "L", "XL", "XXL"]),
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
                        "https://images.unsplash.com/photo-1503342394128-c104d54dba01?w=400"
                    ]),
                    stock=100,
                    is_active=True
                ),
                models.Product(
                    code="DJ001",
                    name="Classic Denim Jacket",
                    description="A timeless denim jacket that never goes out of style. Perfect for layering and adding a casual touch to any outfit.",
                    price=45.99,
                    original_price=69.99,
                    category="Jackets",
                    color="Blue",
                    sizes=json.dumps(["S", "M", "L", "XL"]),
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1548126032-079a0fb009e9?w=400",
                        "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400"
                    ]),
                    stock=50,
                    is_active=True
                ),
                models.Product(
                    code="CH001",
                    name="Slim Fit Chinos",
                    description="Comfortable and stylish slim fit chinos, perfect for both casual and semi-formal occasions.",
                    price=32.99,
                    original_price=49.99,
                    category="Pants",
                    color="Khaki",
                    sizes=json.dumps(["30", "32", "34", "36", "38"]),
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400",
                        "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400"
                    ]),
                    stock=75,
                    is_active=True
                ),
                models.Product(
                    code="HS001",
                    name="Hooded Sweatshirt",
                    description="Cozy and warm hoodie with a modern fit. Perfect for casual days and chilly evenings.",
                    price=28.99,
                    original_price=39.99,
                    category="Sweatshirts",
                    color="Gray",
                    sizes=json.dumps(["S", "M", "L", "XL"]),
                    images=json.dumps([
                        "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
                        "https://images.unsplash.com/photo-1578768079052-aa76e52ff62e?w=400"
                    ]),
                    stock=60,
                    is_active=True
                )
            ]
            
            for product in sample_products:
                db.add(product)
            
            db.commit()
            print(f"✅ Added {len(sample_products)} sample products")
        
        print("\n🎉 Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()