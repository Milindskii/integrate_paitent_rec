import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
import crud
from database import get_db

router = APIRouter()


# ─── Doctors ─────────────────────────────────────────────────────────────────

@router.post("/doctors/", response_model=schemas.Doctor, status_code=201, tags=["Doctors"])
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """Add a new doctor. POST /api/doctors/"""
    return crud.create_doctor(db, doctor)

@router.get("/doctors/", response_model=List[schemas.Doctor], tags=["Doctors"])
def list_doctors(db: Session = Depends(get_db)):
    """Get all doctors. GET /api/doctors/"""
    return crud.get_doctors(db)

@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor, tags=["Doctors"])
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ─── Departments ─────────────────────────────────────────────────────────────

@router.post("/departments/", response_model=schemas.Department, status_code=201, tags=["Departments"])
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, dept)

@router.get("/departments/", response_model=List[schemas.Department], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)


# ─── Appointments ─────────────────────────────────────────────────────────────

@router.post("/appointments/", response_model=schemas.Appointment, status_code=201, tags=["Appointments"])
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appt)

@router.get("/appointments/", response_model=List[schemas.Appointment], tags=["Appointments"])
def list_appointments(db: Session = Depends(get_db)):
    """Get all appointments. GET /api/appointments/"""
    return crud.get_appointments(db)

@router.get("/appointments/doctor/{doctor_id}", response_model=List[schemas.Appointment], tags=["Appointments"])
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    """Get appointments for a specific doctor. GET /api/appointments/doctor/{doctorId}"""
    return crud.get_doctor_appointments(db, doctor_id)

@router.put("/appointments/{appt_id}/status", response_model=schemas.Appointment, tags=["Appointments"])
def update_appointment_status(appt_id: int, status_update: schemas.AppointmentStatusUpdate, db: Session = Depends(get_db)):
    updated = crud.update_appointment_status(db, appt_id, status_update.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated


# ─── Medical Records ──────────────────────────────────────────────────────────

@router.post("/medical-records/", response_model=schemas.MedicalRecord, status_code=201, tags=["Medical Records"])
def create_medical_record(record: schemas.MedicalRecordCreate, db: Session = Depends(get_db)):
    return crud.create_medical_record(db, record)

@router.get("/medical-records/{record_id}", response_model=schemas.MedicalRecord, tags=["Medical Records"])
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_medical_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


# ─── Prescriptions ───────────────────────────────────────────────────────────

@router.post("/prescriptions/", response_model=schemas.Prescription, status_code=201, tags=["Prescriptions"])
def create_prescription(rx: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_prescription(db, rx)


# ─── Lab Tests ───────────────────────────────────────────────────────────────

@router.post("/lab-tests/", response_model=schemas.LabTest, status_code=201, tags=["Lab Tests"])
def create_lab_test(lab: schemas.LabTestCreate, db: Session = Depends(get_db)):
    return crud.create_lab_test(db, lab)

@router.put("/lab-tests/{test_id}/result", response_model=schemas.LabTest, tags=["Lab Tests"])
def update_lab_result(test_id: int, result: schemas.LabResultUpdate, db: Session = Depends(get_db)):
    updated = crud.update_lab_result(db, test_id, result.result, result.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Test not found")
    return updated


# ─── Billing ─────────────────────────────────────────────────────────────────

@router.post("/billing/", response_model=schemas.Bill, status_code=201, tags=["Billing"])
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    return crud.create_bill(db, bill)

@router.put("/billing/{bill_id}/pay", response_model=schemas.Bill, tags=["Billing"])
def pay_bill(bill_id: int, db: Session = Depends(get_db)):
    updated = crud.pay_bill(db, bill_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Bill not found")
    return updated


# ─── Dashboard ───────────────────────────────────────────────────────────────

@router.get("/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Dashboard statistics. GET /api/dashboard/stats"""
    return crud.get_dashboard_stats(db)
