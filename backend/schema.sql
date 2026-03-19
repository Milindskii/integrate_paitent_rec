-- ============================================================
--  Integrated Patient Record & Treatment History DBMS
--  PostgreSQL Schema
--  SRM Institute of Science and Technology, Ramapuram
-- ============================================================

-- Create the database (run this separately as superuser)
-- CREATE DATABASE patient_records_db;

-- Enable UUID extension (optional, using serial for simplicity)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ─── DEPARTMENTS ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS departments (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── DOCTORS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doctors (
    id               SERIAL PRIMARY KEY,
    name             VARCHAR(150) NOT NULL,
    specialization   VARCHAR(100) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    phone            VARCHAR(20),
    department_id    INT REFERENCES departments(id) ON DELETE SET NULL,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ─── PATIENTS ───────────────────────────────────────────────
-- UPDATED: Added medical_conditions and password_hash columns
CREATE TABLE IF NOT EXISTS patients (
    id                      SERIAL PRIMARY KEY,
    name                    VARCHAR(150) NOT NULL,
    date_of_birth           DATE NOT NULL,
    gender                  VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')) NOT NULL,
    blood_group             VARCHAR(5),
    phone                   VARCHAR(20) NOT NULL,
    email                   VARCHAR(150),
    address                 TEXT,
    emergency_contact_name  VARCHAR(150),
    emergency_contact_phone VARCHAR(20),
    allergies               TEXT,
    medical_conditions      TEXT,                    -- NEW COLUMN: Pre-existing conditions
    password_hash           VARCHAR(255) NOT NULL,   -- NEW COLUMN: Hashed password for authentication
    created_at              TIMESTAMPTZ DEFAULT NOW(),
    updated_at              TIMESTAMPTZ
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_patients_updated_at ON patients;

CREATE TRIGGER trg_patients_updated_at
BEFORE UPDATE ON patients
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ─── APPOINTMENTS ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appointments (
    id                SERIAL PRIMARY KEY,
    patient_id        INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id         INT NOT NULL REFERENCES doctors(id) ON DELETE SET NULL,
    appointment_date  DATE NOT NULL,
    appointment_time  VARCHAR(10) NOT NULL,
    reason            TEXT,
    status            VARCHAR(20) DEFAULT 'scheduled'
                        CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes             TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ─── MEDICAL RECORDS (Treatment History) ───────────────────
CREATE TABLE IF NOT EXISTS medical_records (
    id                SERIAL PRIMARY KEY,
    patient_id        INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    doctor_id         INT NOT NULL REFERENCES doctors(id),
    visit_date        DATE NOT NULL,
    chief_complaint   TEXT NOT NULL,
    diagnosis         TEXT NOT NULL,
    treatment_given   TEXT,
    follow_up_date    DATE,
    notes             TEXT,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ─── PRESCRIPTIONS ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS prescriptions (
    id                SERIAL PRIMARY KEY,
    patient_id        INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    medical_record_id INT REFERENCES medical_records(id) ON DELETE SET NULL,
    medication_name   VARCHAR(200) NOT NULL,
    dosage            VARCHAR(100) NOT NULL,
    frequency         VARCHAR(100) NOT NULL,
    duration_days     INT,
    instructions      TEXT,
    prescribed_date   DATE NOT NULL,
    created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- ─── LAB TESTS ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lab_tests (
    id              SERIAL PRIMARY KEY,
    patient_id      INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    test_name       VARCHAR(200) NOT NULL,
    ordered_date    DATE NOT NULL,
    result          TEXT,
    status          VARCHAR(20) DEFAULT 'pending'
                      CHECK (status IN ('pending', 'completed')),
    reference_range VARCHAR(200),
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── BILLS ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bills (
    id          SERIAL PRIMARY KEY,
    patient_id  INT NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL,
    bill_date   DATE NOT NULL,
    status      VARCHAR(10) DEFAULT 'pending'
                  CHECK (status IN ('pending', 'paid')),
    paid_on     DATE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── INDEXES FOR PERFORMANCE ────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_patients_name       ON patients(name);
CREATE INDEX IF NOT EXISTS idx_patients_blood_group ON patients(blood_group);
CREATE INDEX IF NOT EXISTS idx_patients_email      ON patients(email);                    -- NEW INDEX
CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor  ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date    ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_medical_records_patient ON medical_records(patient_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_patient   ON prescriptions(patient_id);
CREATE INDEX IF NOT EXISTS idx_lab_tests_patient       ON lab_tests(patient_id);
CREATE INDEX IF NOT EXISTS idx_bills_patient           ON bills(patient_id);

-- ─── SEED DATA ──────────────────────────────────────────────
INSERT INTO departments (name, description) VALUES
  ('Cardiology',     'Heart and cardiovascular diseases'),
  ('Neurology',      'Brain and nervous system disorders'),
  ('Orthopedics',    'Bone, joint, and muscle conditions'),
  ('General Medicine', 'Primary and general healthcare'),
  ('Pathology / Lab',  'Laboratory investigations and diagnostics')
ON CONFLICT (name) DO NOTHING;

INSERT INTO doctors (name, specialization, email, phone, department_id) VALUES
  ('Dr. Ramesh Kumar',  'Cardiologist',   'ramesh.kumar@hospital.com',  '9876543210', 1),
  ('Dr. Priya Sharma',  'Neurologist',    'priya.sharma@hospital.com',  '9876543211', 2),
  ('Dr. Anil Mehta',    'Orthopedic Surgeon', 'anil.mehta@hospital.com','9876543212', 3),
  ('Dr. Suresh Patel',  'General Physician', 'suresh.patel@hospital.com','9876543213', 4)
ON CONFLICT (email) DO NOTHING;

-- ─── SAMPLE PATIENT (for testing) ───────────────────────────
-- Note: Password_hash is a bcrypt hash of 'password123'
-- You can add this after running the schema
/*
INSERT INTO patients (
    name, date_of_birth, gender, blood_group, phone, email, 
    address, emergency_contact_name, emergency_contact_phone, 
    allergies, medical_conditions, password_hash
) VALUES (
    'John Doe', '1990-01-15', 'male', 'O+', '9876543214', 
    'john.doe@example.com', '123 Main St, City', 'Jane Doe', '9876543215',
    'Penicillin', 'Asthma', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NQqKxJH.K'
);
*/