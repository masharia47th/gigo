from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User as DbUser  # Import the SQLAlchemy User model
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/register-user", response_model=UserSchema)
async def register_user(user: UserCreate, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    db_user = DbUser(username=user.username, email=user.email, hashed_password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[UserSchema])
async def list_users(db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    users = db.query(DbUser).all()
    return users

@router.delete("/delete-user/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user

@router.put("/update-user/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: DbUser = Depends(get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user_update.dict().items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
