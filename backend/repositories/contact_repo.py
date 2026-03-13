from sqlalchemy.orm import Session
from backend.models import ContactMessage

class ContactRepository:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ContactMessage]:
        return db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, db: Session, contact_data: dict) -> ContactMessage:
        db_contact = ContactMessage(**contact_data)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
