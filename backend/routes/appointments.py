import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db

router = APIRouter()


# ─── List / Create Appointments ───────────────────────────────────────────────

@router.get("/", response_model=List[schemas.Appointment])
def list_appointments(skip: int = 0, limit: int = 500, db: Session = Depends(get_db)):
    return crud.get_appointments(db, skip, limit)

@router.post("/", response_model=schemas.Appointment, status_code=201)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appt)


# ─── Get / Update / Delete Single Appointment ────────────────────────────────

@router.get("/{appt_id}", response_model=schemas.Appointment)
def get_appointment(appt_id: int, db: Session = Depends(get_db)):
    a = crud.get_appointment(db, appt_id)
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a

@router.put("/{appt_id}", response_model=schemas.Appointment)
def update_appointment(appt_id: int, data: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    a = crud.update_appointment(db, appt_id, data)
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a

@router.put("/{appt_id}/status", response_model=schemas.Appointment)
def update_status(appt_id: int, data: schemas.AppointmentStatusUpdate, db: Session = Depends(get_db)):
    a = crud.update_appointment_status(db, appt_id, data.status, data.notes)
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return a

@router.delete("/{appt_id}")
def delete_appointment(appt_id: int, db: Session = Depends(get_db)):
    if not crud.delete_appointment(db, appt_id):
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted"}


# ─── Scoped Appointment Queries ───────────────────────────────────────────────

@router.get("/patient/{patient_id}", response_model=List[schemas.Appointment])
def get_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_patient_appointments(db, patient_id)

@router.get("/doctor/{doctor_id}", response_model=List[schemas.Appointment])
def get_by_doctor(doctor_id: int, date: Optional[str] = None, db: Session = Depends(get_db)):
    from datetime import datetime
    date_filter = None
    if date:
        try:
            date_filter = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            pass
    return crud.get_doctor_appointments(db, doctor_id, date_filter)
