from app.database import SessionLocal
from app import models
import json

def add_test_products():
    db = SessionLocal()
    
    # Check if products already exist
    if db.query(models.Product).count() > 0:
        print("Products already exist. Skipping...")
        db.close()
        return
    
    # Sample products
    products = [
        {
            "code": "TS001",
            "name": "Regular Fit T-Shirt",
            "description": "The Men's Short-Sleeve Fitted T-shirt is the perfect choice for those who love a neat, dynamic style. With a basic yet sophisticated design, the shirt is easily combined with various outfits, suitable for both work and casual outings.",
            "price": 8.95,
            "original_price": 13.59,
            "category": "T-Shirts",
            "color": "Green",
            "sizes": json.dumps(["S", "M", "L", "XL", "XXL"]),
            "images": json.dumps([
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
                "https://images.unsplash.com/photo-1503342394128-c104d54dba01?w=400"
            ]),
            "stock": 100,
            "is_active": True
        },
        {
            "code": "DJ001",
            "name": "Classic Denim Jacket",
            "description": "A timeless denim jacket that never goes out of style. Perfect for layering and adding a casual touch to any outfit.",
            "price": 45.99,
            "original_price": 69.99,
            "category": "Jackets",
            "color": "Blue",
            "sizes": json.dumps(["S", "M", "L", "XL"]),
            "images": json.dumps([
                "https://images.unsplash.com/photo-1548126032-079a0fb009e9?w=400",
                "https://images.unsplash.com/photo-1551537482-f2075a1d41f2?w=400"
            ]),
            "stock": 50,
            "is_active": True
        },
        {
            "code": "CH001",
            "name": "Slim Fit Chinos",
            "description": "Comfortable and stylish slim fit chinos, perfect for both casual and semi-formal occasions.",
            "price": 32.99,
            "original_price": 49.99,
            "category": "Pants",
            "color": "Khaki",
            "sizes": json.dumps(["30", "32", "34", "36", "38"]),
            "images": json.dumps([
                "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400",
                "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400"
            ]),
            "stock": 75,
            "is_active": True
        },
        {
            "code": "HS001",
            "name": "Hooded Sweatshirt",
            "description": "Cozy and warm hoodie with a modern fit. Perfect for casual days and chilly evenings.",
            "price": 28.99,
            "original_price": 39.99,
            "category": "Sweatshirts",
            "color": "Gray",
            "sizes": json.dumps(["S", "M", "L", "XL"]),
            "images": json.dumps([
                "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
                "https://images.unsplash.com/photo-1578768079052-aa76e52ff62e?w=400"
            ]),
            "stock": 60,
            "is_active": True
        }
    ]
    
    for product_data in products:
        product = models.Product(**product_data)
        db.add(product)
    
    db.commit()
    print(f"Added {len(products)} test products!")
    db.close()

if __name__ == "__main__":
    add_test_products()