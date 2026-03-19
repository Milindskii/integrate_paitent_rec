import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, crud
from database import get_db

router = APIRouter()

# ─── Departments ─────────────────────────────────────────────────────────────

@router.post("/departments/", response_model=schemas.Department, status_code=201, tags=["Departments"])
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, dept)

@router.get("/departments/", response_model=List[schemas.Department], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)

# ─── Medical Records ─────────────────────────────────────────────────────────

@router.post("/medical-records/", response_model=schemas.MedicalRecord, status_code=201, tags=["Medical Records"])
def create_medical_record(record: schemas.MedicalRecordCreate, db: Session = Depends(get_db)):
    return crud.create_medical_record(db, record)

@router.get("/medical-records/{record_id}", response_model=schemas.MedicalRecord, tags=["Medical Records"])
def get_medical_record(record_id: int, db: Session = Depends(get_db)):
    r = crud.get_medical_record(db, record_id)
    if not r:
        raise HTTPException(status_code=404, detail="Record not found")
    return r

# ─── Prescriptions ────────────────────────────────────────────────────────────

@router.post("/prescriptions/", response_model=schemas.Prescription, status_code=201, tags=["Prescriptions"])
def create_prescription(rx: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_prescription(db, rx)

# ─── Lab Tests ────────────────────────────────────────────────────────────────

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

# ─── Dashboard ────────────────────────────────────────────────────────────────

@router.get("/dashboard/stats", tags=["Dashboard"])
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)
