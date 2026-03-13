from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend import schemas
from backend.database import get_db
from backend.services.admin_service import AdminService
from backend.services.product_service import ProductService
from backend.services.contact_service import ContactService
from backend.models import AdminUser

router = APIRouter(prefix="/admin", tags=["admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

admin_service = AdminService()
product_service = ProductService()
contact_service = ContactService()

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return admin_service.get_current_admin(db, token)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return admin_service.authenticate_admin(db, form_data.username, form_data.password)

# ── Products ──────────────────────────────────────────────────────────────────

@router.get("/products", response_model=list[schemas.ProductResponse])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return product_service.get_products(db, skip=skip, limit=limit)

@router.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return product_service.create_product(db, product.dict())

@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return product_service.update_product(db, product_id, product.dict(exclude_unset=True))

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return product_service.delete_product(db, product_id)

# ── Contacts ──────────────────────────────────────────────────────────────────

@router.get("/contacts", response_model=list[schemas.ContactMessageResponse])
def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return contact_service.get_contacts(db, skip=skip, limit=limit)

# ── Users ─────────────────────────────────────────────────────────────────────

@router.get("/users", response_model=list[schemas.AdminUserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    return admin_service.get_users(db, skip=skip, limit=limit)

