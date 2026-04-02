from app.database import SessionLocal
from app import models
from app.auth import get_password_hash

def create_admin():
    db = SessionLocal()
    
    # Check if admin already exists
    admin = db.query(models.User).filter(models.User.email == "admin123@gmail.com").first()
    
    if admin:
        print("Admin user already exists!")
        db.close()
        return
    
    # Create admin user
    admin_user = models.User(
        email="admin123@gmail.com",
        hashed_password=get_password_hash("admin123"),
        is_admin=True
    )
    
    db.add(admin_user)
    db.commit()
    print("Admin user created successfully!")
    print("Email: admin123@gmail.com")
    print("Password: admin123")
    db.close()

if __name__ == "__main__":
    create_admin()