from sqlalchemy.orm import Session
from backend.models import Product

class ProductRepository:
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, product_id: int) -> Product | None:
        return db.query(Product).filter(Product.id == product_id).first()

    def create(self, db: Session, product_data: dict) -> Product:
        db_product = Product(**product_data)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update(self, db: Session, db_product: Product, update_data: dict) -> Product:
        for key, value in update_data.items():
            if value is not None:
                setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    def delete(self, db: Session, db_product: Product) -> None:
        db.delete(db_product)
        db.commit()

