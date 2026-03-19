import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db
from auth import create_access_token

router = APIRouter()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


# ─── Admin Login ──────────────────────────────────────────────────────────────

@router.post("/auth/login", response_model=schemas.Token)
def admin_login(login: schemas.AdminLogin):
    if login.username != ADMIN_USERNAME or login.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    token = create_access_token({"sub": "0", "role": "admin", "name": "Administrator"})
    return schemas.Token(
        access_token=token,
        user=schemas.TokenUser(id=0, name="Administrator", email="admin@medisync.com", role="admin")
    )


# ─── System Stats ─────────────────────────────────────────────────────────────

@router.get("/stats")
def admin_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)
