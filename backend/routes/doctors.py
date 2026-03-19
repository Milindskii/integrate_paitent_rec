import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db
from auth import create_access_token

router = APIRouter()


# ─── Doctor Login ─────────────────────────────────────────────────────────────

@router.post("/auth/login", response_model=schemas.Token)
def doctor_login(login: schemas.DoctorLogin, db: Session = Depends(get_db)):
    doctor = crud.authenticate_doctor(db, login.email, login.password)
    if not doctor:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(doctor.id), "role": "doctor", "name": doctor.name})
    return schemas.Token(
        access_token=token,
        user=schemas.TokenUser(
            id=doctor.id, name=doctor.name, email=doctor.email, role="doctor",
            specialization=doctor.specialization, department_id=doctor.department_id
        )
    )


# ─── List / Create Doctors ────────────────────────────────────────────────────

@router.get("/", response_model=List[schemas.Doctor])
def list_doctors(db: Session = Depends(get_db)):
    return crud.get_doctors(db)

@router.post("/", response_model=schemas.Doctor, status_code=201)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    if crud.get_doctor_by_email(db, doctor.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_doctor(db, doctor)


# ─── Get / Update / Delete Single Doctor ─────────────────────────────────────

@router.get("/{doctor_id}", response_model=schemas.Doctor)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    d = crud.get_doctor(db, doctor_id)
    if not d:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return d

@router.put("/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(doctor_id: int, data: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    d = crud.update_doctor(db, doctor_id, data)
    if not d:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return d

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    if not crud.deactivate_doctor(db, doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deactivated successfully"}


# ─── Doctor Sub-routes ────────────────────────────────────────────────────────

@router.get("/{doctor_id}/appointments", response_model=List[schemas.Appointment])
def get_doctor_appointments(doctor_id: int, date: Optional[str] = None, db: Session = Depends(get_db)):
    from datetime import datetime
    date_filter = None
    if date:
        try:
            date_filter = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            pass
    return crud.get_doctor_appointments(db, doctor_id, date_filter)

@router.get("/{doctor_id}/stats", response_model=schemas.DoctorStats)
def get_doctor_stats(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_stats(db, doctor_id)
