import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db
from auth import create_access_token, get_current_user, require_admin

router = APIRouter()


# ─── Patient Registration ─────────────────────────────────────────────────────

@router.post("/register", response_model=schemas.Patient, status_code=201)
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    if patient.email:
        if crud.get_patient_by_email(db, patient.email):
            raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_patient(db, patient)


# ─── Patient Login ────────────────────────────────────────────────────────────

@router.post("/auth/login", response_model=schemas.Token)
def patient_login(login: schemas.PatientLogin, db: Session = Depends(get_db)):
    patient = crud.authenticate_patient(db, login.email, login.password)
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(patient.id), "role": "patient", "name": patient.name})
    return schemas.Token(
        access_token=token,
        user=schemas.TokenUser(id=patient.id, name=patient.name, email=patient.email, role="patient")
    )


# ─── List All Patients (admin) ────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.Patient])
def list_patients(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip, limit)


# ─── Search Patients ──────────────────────────────────────────────────────────

@router.get("/search/", response_model=List[schemas.Patient])
def search_patients(name: Optional[str] = None, blood_group: Optional[str] = None,
                    db: Session = Depends(get_db)):
    return crud.search_patients(db, name, blood_group)


# ─── Get / Update / Delete Single Patient ────────────────────────────────────

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = crud.get_patient(db, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, data: schemas.PatientUpdate, db: Session = Depends(get_db)):
    p = crud.update_patient(db, patient_id, data)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    if not crud.deactivate_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deactivated successfully"}


# ─── Patient Sub-routes ───────────────────────────────────────────────────────

@router.get("/{patient_id}/appointments", response_model=List[schemas.Appointment])
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_appointments(db, patient_id)

@router.get("/{patient_id}/medical-records", response_model=List[schemas.MedicalRecord])
def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_medical_records(db, patient_id)

@router.get("/{patient_id}/prescriptions", response_model=List[schemas.Prescription])
def get_patient_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_prescriptions(db, patient_id)

@router.get("/{patient_id}/lab-tests", response_model=List[schemas.LabTest])
def get_patient_lab_tests(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_lab_tests(db, patient_id)

@router.get("/{patient_id}/bills", response_model=List[schemas.Bill])
def get_patient_bills(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_bills(db, patient_id)
