import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal
from backend.models import AdminUser
from backend.auth import get_password_hash

def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == "admin@nexconnect.io").first()
        if not admin:
            hashed_pw = get_password_hash("admin")
            new_admin = AdminUser(username="admin@nexconnect.io", hashed_password=hashed_pw)
            db.add(new_admin)
            db.commit()
            print("Default admin created: admin@nexconnect.io / admin")
        else:
            print("Admin user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_admin()
