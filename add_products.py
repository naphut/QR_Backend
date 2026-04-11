import requests
import json

# Backend URL
BACKEND_URL = "https://qr-backend-3ula.onrender.com"

# Sample products
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
        "stock": 100
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
        "stock": 50
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
        "stock": 30
    }
]

print("Adding sample products...")

for product in products:
    try:
        # Try to add product without auth first (if endpoint allows)
        response = requests.post(f"{BACKEND_URL}/api/products/", json=product)
        
        if response.status_code == 200:
            print(f"✅ Added: {product['name']}")
        else:
            print(f"❌ Failed to add {product['name']}: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error adding {product['name']}: {e}")

print("\nChecking products endpoint...")
try:
    response = requests.get(f"{BACKEND_URL}/api/products/")
    print(f"Products count: {len(response.json())}")
    print(f"Products: {response.json()}")
except Exception as e:
    print(f"Error checking products: {e}")
