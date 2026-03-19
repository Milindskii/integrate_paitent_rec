import sys
import os

# Ensure parent backend directory is on the path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
import crud
from database import get_db

router = APIRouter()


# ─── Patient Registration ────────────────────────────────────────────────────

@router.post("/register", response_model=schemas.Patient, status_code=201)
async def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Register a new patient. POST /api/patients/register"""
    try:
        if patient.email:
            existing = crud.get_patient_by_email(db, patient.email)
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")
        return crud.create_patient(db=db, patient=patient)
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ─── Patient Login ───────────────────────────────────────────────────────────

@router.post("/auth/login", response_model=schemas.Token)
def login(login_data: schemas.LoginData, db: Session = Depends(get_db)):
    """Patient (or doctor) login. POST /api/patients/auth/login"""
    user = crud.authenticate_user(db, login_data.email, login_data.password, login_data.role)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": f"session_{user.id}_{login_data.role}",
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.name,
        "role": login_data.role,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": login_data.role,
        },
    }


# ─── Get All Patients ────────────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.Patient])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all patients. GET /api/patients/"""
    return crud.get_patients(db, skip, limit)


# ─── Search Patients ─────────────────────────────────────────────────────────

@router.get("/search/", response_model=List[schemas.Patient])
def search_patients(
    name: Optional[str] = None,
    blood_group: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.search_patients(db, name, blood_group)


# ─── Get Single Patient ──────────────────────────────────────────────────────
# NOTE: wildcard route must come AFTER all fixed-path routes above

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get a single patient by ID. GET /api/patients/{patient_id}"""
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
