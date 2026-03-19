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
    password: Optional[str] = None   # Optional — set a temp password when admin adds doctor

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    password: Optional[str] = None

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    email: str
    phone: Optional[str] = None
    department_id: Optional[int] = None
    is_active: bool = True
    created_at: datetime
    class Config:
        from_attributes = True

class DoctorStats(BaseModel):
    total_patients: int
    total_appointments: int
    scheduled_today: int
    completed_today: int


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
    password: str

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    password: Optional[str] = None

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
    is_active: bool = True
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

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[AppointmentStatusEnum] = None

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatusEnum
    notes: Optional[str] = None

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

class PatientLogin(BaseModel):
    email: str
    password: str

class DoctorLogin(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

# Legacy: keep for backward compat
class LoginData(BaseModel):
    email: str
    password: str
    role: str

class TokenUser(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    role: str
    specialization: Optional[str] = None
    department_id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: TokenUser


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