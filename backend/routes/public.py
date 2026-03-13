from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend import schemas
from backend.database import get_db
from backend.services.product_service import ProductService
from backend.services.contact_service import ContactService

router = APIRouter(prefix="/api/v1", tags=["public"])

product_service = ProductService()
contact_service = ContactService()

@router.get("/products", response_model=list[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_service.get_products(db, skip=skip, limit=limit)

@router.post("/contact", response_model=schemas.ContactMessageResponse)
def submit_contact(contact: schemas.ContactMessageCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return contact_service.process_contact(db, background_tasks, contact.dict())
