from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db

router = APIRouter()

# ─────────────────────────────────────────────
# PATIENTS
# ─────────────────────────────────────────────

@router.post("/patients/", response_model=schemas.Patient, status_code=201, tags=["Patients"])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@router.get("/patients/", response_model=List[schemas.Patient], tags=["Patients"])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_patients(db, skip, limit)

@router.put("/patients/{patient_id}", response_model=schemas.Patient, tags=["Patients"])
def update_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    updated = crud.update_patient(db, patient_id, patient)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@router.delete("/patients/{patient_id}", tags=["Patients"])
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    if not crud.delete_patient(db, patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}

@router.get("/patients/search/", response_model=List[schemas.Patient], tags=["Patients"])
def search_patients(name: Optional[str] = None, blood_group: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.search_patients(db, name, blood_group)

# ─────────────────────────────────────────────
# DOCTORS
# ─────────────────────────────────────────────

@router.post("/doctors/", response_model=schemas.Doctor, status_code=201, tags=["Doctors"])
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)

@router.get("/doctors/", response_model=List[schemas.Doctor], tags=["Doctors"])
def list_doctors(db: Session = Depends(get_db)):
    return crud.get_doctors(db)

@router.get("/doctors/{doctor_id}", response_model=schemas.Doctor, tags=["Doctors"])
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# ─────────────────────────────────────────────
# DEPARTMENTS
# ─────────────────────────────────────────────

@router.post("/departments/", response_model=schemas.Department, status_code=201, tags=["Departments"])
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, dept)

@router.get("/departments/", response_model=List[schemas.Department], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)

# ─────────────────────────────────────────────
# APPOINTMENTS
# ─────────────────────────────────────────────

@router.post("/appointments/", response_model=schemas.Appointment, status_code=201, tags=["Appointments"])
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appt)

@router.get("/appointments/", response_model=List[schemas.Appointment], tags=["Appointments"])
def list_appointments(db: Session = Depends(get_db)):
    return crud.get_appointments(db)

@router.put("/appointments/{appt_id}/status", response_model=schemas.Appointment, tags=["Appointments"])
def update_appointment_status(appt_id: int, status_update: schemas.AppointmentStatusUpdate, db: Session = Depends(get_db)):
    updated = crud.update_appointment_status(db, appt_id, status_update.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return updated

# ─────────────────────────────────────────────
# MEDICAL RECORDS (Treatment History)
# ─────────────────────────────────────────────

@router.post("/medical-records/", response_model=schemas.MedicalRecord, status_code=201, tags=["Medical Records"])
def create_medical_record(record: schemas.MedicalRecordCreate, db: Session = Depends(get_db)):
    return crud.create_medical_record(db, record)

@router.get("/medical-records/{record_id}", response_model=schemas.MedicalRecord, tags=["Medical Records"])
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_medical_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

# ─────────────────────────────────────────────
# PRESCRIPTIONS
# ─────────────────────────────────────────────

@router.post("/prescriptions/", response_model=schemas.Prescription, status_code=201, tags=["Prescriptions"])
def create_prescription(rx: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_prescription(db, rx)

# ─────────────────────────────────────────────
# LAB TESTS
# ─────────────────────────────────────────────

@router.post("/lab-tests/", response_model=schemas.LabTest, status_code=201, tags=["Lab Tests"])
def create_lab_test(lab: schemas.LabTestCreate, db: Session = Depends(get_db)):
    return crud.create_lab_test(db, lab)

@router.put("/lab-tests/{test_id}/result", response_model=schemas.LabTest, tags=["Lab Tests"])
def update_lab_result(test_id: int, result: schemas.LabResultUpdate, db: Session = Depends(get_db)):
    updated = crud.update_lab_result(db, test_id, result.result, result.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Test not found")
    return updated

# ─────────────────────────────────────────────
# BILLING
# ─────────────────────────────────────────────

@router.post("/billing/", response_model=schemas.Bill, status_code=201, tags=["Billing"])
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    return crud.create_bill(db, bill)

@router.put("/billing/{bill_id}/pay", response_model=schemas.Bill, tags=["Billing"])
def pay_bill(bill_id: int, db: Session = Depends(get_db)):
    updated = crud.pay_bill(db, bill_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Bill not found")
    return updated

# ─────────────────────────────────────────────
# DASHBOARD / REPORTS
# ─────────────────────────────────────────────

@router.get("/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)
