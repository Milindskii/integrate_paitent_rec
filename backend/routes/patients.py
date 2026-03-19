from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List
import sys
import os

# Ensure parent directory is in sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import schemas, crud
from database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.Patient)
async def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    try:
        # Check if patient already exists
        if patient.email:
            existing_patient = crud.get_patient_by_email(db, patient.email)
            if existing_patient:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new patient (password will be hashed in crud.create_patient)
        new_patient = crud.create_patient(db=db, patient=patient)
        
        return new_patient
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error registering patient: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# ─── Patient Aggregated Report ────────────────────────────────────────────────

@router.get("/reports/patient/{patient_id}", response_model=schemas.PatientReport)
def get_patient_report(patient_id: int, db: Session = Depends(get_db)):
    report = crud.get_patient_report(db, patient_id)
    if not report:
        raise HTTPException(status_code=404, detail="Patient report not found")
    return report

# ─── Authentication ───────────────────────────────────────────────────────────

@router.post("/auth/login", response_model=schemas.Token)
def login(login_data: schemas.LoginData, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data.email, login_data.password, login_data.role)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Simple token generation for demo (in production use JWT)
    return {
        "access_token": f"session_{user.id}_{login_data.role}",
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.name,
        "role": login_data.role
    }

