# backend/app/routers/welcome.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Token URL for login

# Caretaker-protected route
@router.get("/caretaker-protected-route")
async def caretaker_protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if user.role != 'care_taker':
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome to Care Taker Dashboard"}

# Admin-protected route
@router.get("/admin-protected-route")
async def admin_protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome to Admin Dashboard"}

@router.get("/tenant-protected-route")
async def tenant_protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if user.role != 'tenant':
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"message": "Welcome to Tenant Dashboard"}