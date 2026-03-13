from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.repositories.product_repo import ProductRepository
from backend.models import Product

class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()

    def get_products(self, db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.product_repo.get_all(db, skip=skip, limit=limit)

    def create_product(self, db: Session, product_data: dict) -> Product:
        return self.product_repo.create(db, product_data)

    def update_product(self, db: Session, product_id: int, update_data: dict) -> Product:
        db_product = self.product_repo.get_by_id(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return self.product_repo.update(db, db_product, update_data)

    def delete_product(self, db: Session, product_id: int) -> dict:
        db_product = self.product_repo.get_by_id(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        self.product_repo.delete(db, db_product)
        return {"detail": "Product deleted successfully"}

