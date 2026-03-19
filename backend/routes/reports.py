from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter()

@router.get("/patient/{patient_id}", response_model=schemas.PatientReport)
def get_patient_report(patient_id: int, db: Session = Depends(get_db)):
    report = crud.get_patient_report(db, patient_id)
    if not report:
        raise HTTPException(status_code=404, detail="Patient report not found")
    return report
