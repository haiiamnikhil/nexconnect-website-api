from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from backend import auth
from backend.repositories.admin_repo import AdminRepository
from backend.models import AdminUser

class AdminService:
    def __init__(self):
        self.admin_repo = AdminRepository()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[AdminUser]:
        return self.admin_repo.get_all(db, skip=skip, limit=limit)

    def get_current_admin(self, db: Session, token: str) -> AdminUser:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except auth.JWTError:
            raise credentials_exception
            
        user = self.admin_repo.get_by_username(db, username=username)
        if user is None:
            raise credentials_exception
        return user

    def authenticate_admin(self, db: Session, username: str, password: str) -> dict:
        user = self.admin_repo.get_by_username(db, username=username)
        if not user or not auth.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
