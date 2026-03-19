from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class AppointmentStatusEnum(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class BillStatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"

class LabStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"


# ─── Department ───────────────────────────────────────────────────────────────

class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Department(DepartmentCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Doctor ───────────────────────────────────────────────────────────────────

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: str
    phone: Optional[str] = None
    department_id: Optional[int] = None

class Doctor(DoctorCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Patient ──────────────────────────────────────────────────────────────────

class PatientCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: GenderEnum
    blood_group: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    password: str   # Required for registration; will be hashed before storing

class Patient(BaseModel):
    id: int
    name: str
    date_of_birth: date
    gender: GenderEnum
    blood_group: Optional[str] = None
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Appointment ──────────────────────────────────────────────────────────────

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: str
    reason: Optional[str] = None
    notes: Optional[str] = None

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatusEnum

class Appointment(AppointmentCreate):
    id: int
    status: AppointmentStatusEnum
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Medical Record ───────────────────────────────────────────────────────────

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    visit_date: date
    chief_complaint: str
    diagnosis: str
    treatment_given: Optional[str] = None
    follow_up_date: Optional[date] = None
    notes: Optional[str] = None

class MedicalRecord(MedicalRecordCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Prescription ─────────────────────────────────────────────────────────────

class PrescriptionCreate(BaseModel):
    patient_id: int
    medical_record_id: Optional[int] = None
    medication_name: str
    dosage: str
    frequency: str
    duration_days: Optional[int] = None
    instructions: Optional[str] = None
    prescribed_date: date

class Prescription(PrescriptionCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Lab Test ─────────────────────────────────────────────────────────────────

class LabTestCreate(BaseModel):
    patient_id: int
    test_name: str
    ordered_date: date
    reference_range: Optional[str] = None
    notes: Optional[str] = None

class LabResultUpdate(BaseModel):
    result: str
    status: LabStatusEnum = LabStatusEnum.completed

class LabTest(LabTestCreate):
    id: int
    result: Optional[str] = None
    status: LabStatusEnum
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Bill ─────────────────────────────────────────────────────────────────────

class BillCreate(BaseModel):
    patient_id: int
    description: str
    amount: float
    bill_date: date

class Bill(BillCreate):
    id: int
    status: BillStatusEnum
    paid_on: Optional[date] = None
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Authentication ────────────────────────────────────────────────────────────

class LoginData(BaseModel):
    email: str
    password: str
    role: str   # "patient" or "doctor"

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    user_name: str
    role: str
    # Frontend expects a nested "user" object as well
    user: dict


# ─── Dashboard ────────────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_patients: int
    total_doctors: int
    total_appointments: int
    scheduled_appointments: int
    total_medical_records: int
    pending_bills: int
    pending_lab_tests: int


# ─── Patient Full Report ──────────────────────────────────────────────────────

class PatientReport(BaseModel):
    patient: Patient
    appointments: List[Appointment] = []
    medical_records: List[MedicalRecord] = []
    prescriptions: List[Prescription] = []
    lab_tests: List[LabTest] = []
    bills: List[Bill] = []

    model_config = {"from_attributes": True}