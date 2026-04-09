import requests

# Backend URL
BACKEND_URL = "https://qr-backend-3ula.onrender.com"

# Create admin user
admin_data = {
    "email": "admin123@gmail.com",
    "password": "admin123",
    "name": "Admin User",
    "is_admin": True
}

try:
    # Register admin user
    response = requests.post(f"{BACKEND_URL}/api/auth/register", json=admin_data)
    print(f"Registration Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Admin user created successfully!")
        
        # Test login
        login_data = {
            "email": "admin123@gmail.com",
            "password": "admin123"
        }
        
        login_response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
    else:
        print("❌ Failed to create admin user")
        
except Exception as e:
    print(f"Error: {e}")
