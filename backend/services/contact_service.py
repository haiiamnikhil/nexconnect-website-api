from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from backend.repositories.contact_repo import ContactRepository
from backend.services.email_service import EmailService
from backend.models import ContactMessage

class ContactService:
    def __init__(self):
        self.contact_repo = ContactRepository()
        self.email_service = EmailService()

    def get_contacts(self, db: Session, skip: int = 0, limit: int = 100) -> list[ContactMessage]:
        return self.contact_repo.get_all(db, skip=skip, limit=limit)

    def process_contact(self, db: Session, background_tasks: BackgroundTasks, contact_data: dict) -> ContactMessage:
        db_contact = self.contact_repo.create(db, contact_data)
        
        # Dispatch emails as a background task
        background_tasks.add_task(
            self.email_service.send_contact_emails,
            name=db_contact.name,
            email=db_contact.email,
            message=db_contact.message
        )
        
        return db_contact
