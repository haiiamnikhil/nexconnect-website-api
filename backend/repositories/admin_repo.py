from sqlalchemy.orm import Session
from backend.models import AdminUser

class AdminRepository:
    def get_by_username(self, db: Session, username: str) -> AdminUser:
        return db.query(AdminUser).filter(AdminUser.username == username).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[AdminUser]:
        return db.query(AdminUser).offset(skip).limit(limit).all()
