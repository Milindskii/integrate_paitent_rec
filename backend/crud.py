import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
import models, schemas


# ─── Password Utilities ───────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ─── Patients ─────────────────────────────────────────────────────────────────

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.email == email).first()

def authenticate_patient(db: Session, email: str, password: str):
    patient = get_patient_by_email(db, email)
    if not patient:
        return None
    if not patient.password_hash or not verify_password(password, patient.password_hash):
        return None
    if not patient.is_active:
        return None
    return patient

def create_patient(db: Session, patient: schemas.PatientCreate):
    data = patient.model_dump()
    password = data.pop("password", "") or "placeholder"
    db_patient = models.Patient(**data, password_hash=hash_password(password))
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patients(db: Session, skip: int = 0, limit: int = 200):
    return db.query(models.Patient).filter(models.Patient.is_active == True).offset(skip).limit(limit).all()

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id, models.Patient.is_active == True).first()

def update_patient(db: Session, patient_id: int, data: schemas.PatientUpdate):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        return None
    update_data = data.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)
    if password:
        p.password_hash = hash_password(password)
    for k, v in update_data.items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

def deactivate_patient(db: Session, patient_id: int):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        return False
    p.is_active = False
    db.commit()
    return True

def search_patients(db: Session, name: str = None, blood_group: str = None):
    q = db.query(models.Patient).filter(models.Patient.is_active == True)
    if name:
        q = q.filter(models.Patient.name.ilike(f"%{name}%"))
    if blood_group:
        q = q.filter(models.Patient.blood_group == blood_group)
    return q.all()


# ─── Doctors ──────────────────────────────────────────────────────────────────

def get_doctor_by_email(db: Session, email: str):
    return db.query(models.Doctor).filter(models.Doctor.email == email).first()

def authenticate_doctor(db: Session, email: str, password: str):
    doctor = get_doctor_by_email(db, email)
    if not doctor:
        return None
    if not doctor.password_hash or not verify_password(password, doctor.password_hash):
        return None
    if not doctor.is_active:
        return None
    return doctor

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    data = doctor.model_dump()
    password = data.pop("password", None) or "Doctor@123"
    db_doctor = models.Doctor(**data, password_hash=hash_password(password))
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_doctors(db: Session):
    return db.query(models.Doctor).filter(models.Doctor.is_active == True).all()

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id, models.Doctor.is_active == True).first()

def update_doctor(db: Session, doctor_id: int, data: schemas.DoctorUpdate):
    d = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not d:
        return None
    update_data = data.model_dump(exclude_unset=True)
    password = update_data.pop("password", None)
    if password:
        d.password_hash = hash_password(password)
    for k, v in update_data.items():
        setattr(d, k, v)
    db.commit()
    db.refresh(d)
    return d

def deactivate_doctor(db: Session, doctor_id: int):
    d = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not d:
        return False
    d.is_active = False
    db.commit()
    return True

def search_doctors(db: Session, name: str = None):
    q = db.query(models.Doctor).filter(models.Doctor.is_active == True)
    if name:
        q = q.filter(models.Doctor.name.ilike(f"%{name}%"))
    return q.all()

def get_doctor_stats(db: Session, doctor_id: int):
    today = date.today()
    total_appointments = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.doctor_id == doctor_id).scalar()
    scheduled_today = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == today,
        models.Appointment.status == models.AppointmentStatusEnum.scheduled).scalar()
    completed_today = db.query(func.count(models.Appointment.id)).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.appointment_date == today,
        models.Appointment.status == models.AppointmentStatusEnum.completed).scalar()
    # Unique patients
    total_patients = db.query(func.count(func.distinct(models.Appointment.patient_id))).filter(
        models.Appointment.doctor_id == doctor_id).scalar()
    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "scheduled_today": scheduled_today,
        "completed_today": completed_today,
    }


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

def get_appointments(db: Session, skip: int = 0, limit: int = 500):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def get_appointment(db: Session, appt_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()

def get_patient_appointments(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).order_by(
        models.Appointment.appointment_date.desc()).all()

def get_doctor_appointments(db: Session, doctor_id: int, date_filter=None):
    q = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id)
    if date_filter:
        q = q.filter(models.Appointment.appointment_date == date_filter)
    return q.order_by(models.Appointment.appointment_date.desc()).all()

def update_appointment(db: Session, appt_id: int, data: schemas.AppointmentUpdate):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(appt, k, v)
    db.commit()
    db.refresh(appt)
    return appt

def update_appointment_status(db: Session, appt_id: int, status: str, notes: str = None):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        return None
    appt.status = status
    if notes:
        appt.notes = notes
    db.commit()
    db.refresh(appt)
    return appt

def delete_appointment(db: Session, appt_id: int):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        return False
    db.delete(appt)
    db.commit()
    return True


# ─── Medical Records ──────────────────────────────────────────────────────────

def create_medical_record(db: Session, record: schemas.MedicalRecordCreate):
    db_record = models.MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_patient_medical_records(db: Session, patient_id: int):
    return db.query(models.MedicalRecord).filter(
        models.MedicalRecord.patient_id == patient_id).order_by(
        models.MedicalRecord.visit_date.desc()).all()

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
    return db.query(models.Prescription).filter(models.Prescription.patient_id == patient_id).order_by(
        models.Prescription.prescribed_date.desc()).all()


# ─── Lab Tests ────────────────────────────────────────────────────────────────

def create_lab_test(db: Session, lab: schemas.LabTestCreate):
    db_lab = models.LabTest(**lab.model_dump())
    db.add(db_lab)
    db.commit()
    db.refresh(db_lab)
    return db_lab

def get_patient_lab_tests(db: Session, patient_id: int):
    return db.query(models.LabTest).filter(models.LabTest.patient_id == patient_id).order_by(
        models.LabTest.ordered_date.desc()).all()

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
    return db.query(models.Bill).filter(models.Bill.patient_id == patient_id).order_by(
        models.Bill.bill_date.desc()).all()

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
    return {
        "total_patients": db.query(func.count(models.Patient.id)).filter(models.Patient.is_active == True).scalar(),
        "total_doctors": db.query(func.count(models.Doctor.id)).filter(models.Doctor.is_active == True).scalar(),
        "total_appointments": db.query(func.count(models.Appointment.id)).scalar(),
        "scheduled_appointments": db.query(func.count(models.Appointment.id)).filter(
            models.Appointment.status == models.AppointmentStatusEnum.scheduled).scalar(),
        "total_medical_records": db.query(func.count(models.MedicalRecord.id)).scalar(),
        "pending_bills": db.query(func.count(models.Bill.id)).filter(
            models.Bill.status == models.BillStatusEnum.pending).scalar(),
        "pending_lab_tests": db.query(func.count(models.LabTest.id)).filter(
            models.LabTest.status == models.LabStatusEnum.pending).scalar(),
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