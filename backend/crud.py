import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
import models, schemas


# ─── Patients ─────────────────────────────────────────────────────────────────

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.email == email).first()


def create_patient(db: Session, patient: schemas.PatientCreate):
    patient_data = patient.model_dump()
    password = patient_data.pop("password", "") or "placeholder_password"

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    db_patient = models.Patient(**patient_data, password_hash=hashed_password)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    print(f"Patient created: {db_patient.name}")
    return db_patient


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()


def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return None

    patient_data = patient.model_dump()
    password = patient_data.pop("password", None)
    if password:
        salt = bcrypt.gensalt()
        db_patient.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    for key, value in patient_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        return False
    db.delete(db_patient)
    db.commit()
    return True


def search_patients(db: Session, name: str = None, blood_group: str = None):
    query = db.query(models.Patient)
    if name:
        query = query.filter(models.Patient.name.ilike(f"%{name}%"))
    if blood_group:
        query = query.filter(models.Patient.blood_group == blood_group)
    return query.all()


# ─── Doctors ──────────────────────────────────────────────────────────────────

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def get_doctors(db: Session):
    return db.query(models.Doctor).all()


def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()


# ─── Departments ──────────────────────────────────────────────────────────────

def create_department(db: Session, dept: schemas.DepartmentCreate):
    db_dept = models.Department(**dept.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept


def get_departments(db: Session):
    return db.query(models.Department).all()


# ─── Appointments ─────────────────────────────────────────────────────────────

def create_appointment(db: Session, appt: schemas.AppointmentCreate):
    db_appt = models.Appointment(**appt.model_dump())
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def get_appointments(db: Session):
    return db.query(models.Appointment).all()


def get_patient_appointments(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()


def get_doctor_appointments(db: Session, doctor_id: int):
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()


def update_appointment_status(db: Session, appt_id: int, status: str):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        return None
    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt


# ─── Medical Records ──────────────────────────────────────────────────────────

def create_medical_record(db: Session, record: schemas.MedicalRecordCreate):
    db_record = models.MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_patient_medical_records(db: Session, patient_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.patient_id == patient_id).all()


def get_medical_record(db: Session, record_id: int):
    return db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()


# ─── Prescriptions ────────────────────────────────────────────────────────────

def create_prescription(db: Session, rx: schemas.PrescriptionCreate):
    db_rx = models.Prescription(**rx.model_dump())
    db.add(db_rx)
    db.commit()
    db.refresh(db_rx)
    return db_rx


def get_patient_prescriptions(db: Session, patient_id: int):
    return db.query(models.Prescription).filter(models.Prescription.patient_id == patient_id).all()


# ─── Lab Tests ────────────────────────────────────────────────────────────────

def create_lab_test(db: Session, lab: schemas.LabTestCreate):
    db_lab = models.LabTest(**lab.model_dump())
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab


def get_patient_lab_tests(db: Session, patient_id: int):
    return db.query(models.LabTest).filter(models.LabTest.patient_id == patient_id).all()


def update_lab_result(db: Session, test_id: int, result: str, status: str):
    test = db.query(models.LabTest).filter(models.LabTest.id == test_id).first()
    if not test:
        return None
    test.result = result
    test.status = status
    db.commit()
    db.refresh(test)
    return test


# ─── Billing ──────────────────────────────────────────────────────────────────

def create_bill(db: Session, bill: schemas.BillCreate):
    db_bill = models.Bill(**bill.model_dump())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


def get_patient_bills(db: Session, patient_id: int):
    return db.query(models.Bill).filter(models.Bill.patient_id == patient_id).all()


def pay_bill(db: Session, bill_id: int):
    bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not bill:
        return None
    bill.status = models.BillStatusEnum.paid
    bill.paid_on = date.today()
    db.commit()
    db.refresh(bill)
    return bill


# ─── Dashboard Stats ──────────────────────────────────────────────────────────

def get_dashboard_stats(db: Session):
    total_patients = db.query(func.count(models.Patient.id)).scalar()
    total_doctors = db.query(func.count(models.Doctor.id)).scalar()
    total_appointments = db.query(func.count(models.Appointment.id)).scalar()
    scheduled_appointments = (
        db.query(func.count(models.Appointment.id))
        .filter(models.Appointment.status == models.AppointmentStatusEnum.scheduled)
        .scalar()
    )
    total_records = db.query(func.count(models.MedicalRecord.id)).scalar()
    pending_bills = (
        db.query(func.count(models.Bill.id))
        .filter(models.Bill.status == models.BillStatusEnum.pending)
        .scalar()
    )
    pending_labs = (
        db.query(func.count(models.LabTest.id))
        .filter(models.LabTest.status == models.LabStatusEnum.pending)
        .scalar()
    )

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "scheduled_appointments": scheduled_appointments,
        "total_medical_records": total_records,
        "pending_bills": pending_bills,
        "pending_lab_tests": pending_labs,
    }


# ─── Aggregated Patient Report ────────────────────────────────────────────────

def get_patient_report(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if not patient:
        return None

    return {
        "patient": patient,
        "appointments": get_patient_appointments(db, patient_id),
        "medical_records": get_patient_medical_records(db, patient_id),
        "prescriptions": get_patient_prescriptions(db, patient_id),
        "lab_tests": get_patient_lab_tests(db, patient_id),
        "bills": get_patient_bills(db, patient_id),
    }


# ─── Authentication ───────────────────────────────────────────────────────────

def authenticate_user(db: Session, email: str, password: str, role: str):
    if role == "patient":
        user = db.query(models.Patient).filter(models.Patient.email == email).first()
    elif role == "doctor":
        user = db.query(models.Doctor).filter(models.Doctor.email == email).first()
    else:
        return None

    if not user:
        return None

    if not hasattr(user, "password_hash") or not user.password_hash:
        return None

    try:
        if bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return user
    except Exception:
        pass

    return None