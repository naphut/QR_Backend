import requests
import json

# Backend URL
BACKEND_URL = "https://qr-backend-3ula.onrender.com"

def manual_init():
    """Manual initialization of the platform"""
    print("🔧 Manual Platform Initialization")
    print("=" * 50)
    
    # Step 1: Create admin user
    print("\n1️⃣ Creating admin user...")
    admin_data = {
        "email": "admin@qrshop.com",
        "password": "admin123",
        "name": "QR Shop Admin"
    }
    
    try:
        register_response = requests.post(f"{BACKEND_URL}/api/auth/register", json=admin_data)
        if register_response.status_code == 200:
            print("✅ Admin user created successfully")
        else:
            print(f"⚠️ Admin might already exist: {register_response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 2: Login
    print("\n2️⃣ Logging in...")
    try:
        login_response = requests.post(f"{BACKEND_URL}/api/auth/login", json=admin_data)
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✅ Login successful")
            headers = {"Authorization": f"Bearer {token}"}
        else:
            print(f"❌ Login failed: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 3: Try to add products via admin endpoint
    print("\n3️⃣ Adding products...")
    
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
    
    success_count = 0
    for product in products:
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/admin/products",
                json=product,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"✅ Added: {product['name']}")
                success_count += 1
            else:
                print(f"❌ Failed {product['name']}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error {product['name']}: {e}")
    
    # Step 4: Test products endpoint
    print("\n4️⃣ Testing products endpoint...")
    try:
        products_response = requests.get(f"{BACKEND_URL}/api/products/")
        if products_response.status_code == 200:
            products_list = products_response.json()
            print(f"✅ Products API working: {len(products_list)} products")
        else:
            print(f"❌ Products API error: {products_response.status_code}")
    except Exception as e:
        print(f"❌ Products test failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 INITIALIZATION SUMMARY:")
    print(f"   Admin User: admin@qrshop.com / admin123")
    print(f"   Products Added: {success_count}/{len(products)}")
    print(f"   Platform Status: {'✅ Ready' if success_count > 0 else '⚠️ Needs manual setup'}")
    
    print("\n🌐 ACCESS URLs:")
    print(f"   Admin Dashboard: https://qr-admin-frontend-zch1.vercel.app")
    print(f"   User Storefront: https://qr-user-frontend007.vercel.app")
    print(f"   Backend API: https://qr-backend-3ula.onrender.com/docs")

if __name__ == "__main__":
    manual_init()
