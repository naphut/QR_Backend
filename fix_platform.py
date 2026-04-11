import requests
import json

# Backend URL
BACKEND_URL = "https://qr-backend-3ula.onrender.com"

def fix_admin_user():
    """Create a new admin user since existing one can't be updated properly"""
    try:
        # Create new admin user with proper admin flag
        admin_data = {
            "email": "admin@qrshop.com",
            "password": "admin123",
            "name": "QR Shop Admin",
            "is_admin": True
        }
        
        register_response = requests.post(f"{BACKEND_URL}/api/auth/register", json=admin_data)
        if register_response.status_code == 200:
            print("✅ New admin user created successfully")
            return True
        else:
            print(f"❌ Failed to create admin: {register_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        return False

def add_test_products():
    """Add test products to the database"""
    
    test_products = [
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
    
    try:
        # Login to get admin token
        login_data = {
            "email": "admin@qrshop.com",
            "password": "admin123"
        }
        
        login_response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        if login_response.status_code != 200:
            print("❌ Cannot login - admin user may not exist")
            return False
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Add products
        success_count = 0
        for product in test_products:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/admin/products",
                    json=product,
                    headers=headers
                )
                
                if response.status_code == 200:
                    print(f"✅ Added product: {product['name']}")
                    success_count += 1
                else:
                    print(f"❌ Failed to add {product['name']}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error adding {product['name']}: {e}")
        
        print(f"\n📊 Summary: {success_count}/{len(test_products)} products added successfully")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing QR E-commerce Platform...")
    print("=" * 50)
    
    # Step 1: Fix admin user
    print("\n1️⃣ Fixing admin user...")
    admin_fixed = fix_admin_user()
    
    # Step 2: Add test products
    print("\n2️⃣ Adding test products...")
    products_added = add_test_products()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 FIX SUMMARY:")
    print(f"   Admin User: {'✅ Fixed' if admin_fixed else '❌ Failed'}")
    print(f"   Test Products: {'✅ Added' if products_added else '❌ Failed'}")
    
    if admin_fixed and products_added:
        print("\n🎉 Platform fixed successfully!")
    else:
        print("\n⚠️  Some issues remain - check the errors above")
