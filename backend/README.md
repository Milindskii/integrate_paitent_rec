# Integrated Patient Record & Treatment History DBMS
### SRM Institute of Science and Technology, Ramapuram | Batch No: 2

---

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Frontend:** React (Vite)

---

## Project Structure

```
patient-rec-system/
├── backend/
│   ├── main.py          ← FastAPI app + all API routes
│   ├── models.py        ← SQLAlchemy ORM models
│   ├── schemas.py       ← Pydantic request/response schemas
│   ├── crud.py          ← Database operations (CRUD)
│   ├── database.py      ← DB connection & session
│   ├── schema.sql       ← PostgreSQL DDL + seed data
│   └── requirements.txt
└── frontend/
    └── src/
        └── App.jsx      ← Complete React frontend
```

---

## Setup Instructions

### 1. PostgreSQL Database

```bash
# Start PostgreSQL and create the database
psql -U postgres
CREATE DATABASE patient_records_db;
\q

# Run the schema (creates tables + seeds departments/doctors)
psql -U postgres -d patient_records_db -f backend/schema.sql
```

### 2. Backend (FastAPI)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set DB connection (or it uses the default below)
export DATABASE_URL="postgresql://postgres:password@localhost:5432/patient_records_db"

# Start the server
uvicorn main:app --reload --port 8000
```

**API Docs:** http://localhost:8000/docs  
**ReDoc:** http://localhost:8000/redoc

### 3. Frontend (React)

```bash
# Create Vite project first (one-time setup)
npm create vite@latest frontend -- --template react
cd frontend
npm install

# Replace src/App.jsx with the provided App.jsx file
# Then start:
npm run dev
```

Frontend runs at: http://localhost:5173

---

## API Endpoints Summary

| Module | Endpoints |
|---|---|
| **Patients** | POST/GET `/patients/` · GET/PUT/DELETE `/patients/{id}` · GET `/patients/search/` |
| **Doctors** | POST/GET `/doctors/` · GET `/doctors/{id}` |
| **Departments** | POST/GET `/departments/` |
| **Appointments** | POST/GET `/appointments/` · PUT `/appointments/{id}/status` |
| **Medical Records** | POST `/medical-records/` · GET `/medical-records/patient/{id}` |
| **Prescriptions** | POST `/prescriptions/` · GET `/prescriptions/patient/{id}` |
| **Lab Tests** | POST `/lab-tests/` · PUT `/lab-tests/{id}/result` |
| **Billing** | POST `/billing/` · PUT `/billing/{id}/pay` |
| **Dashboard** | GET `/dashboard/stats` |
| **Reports** | GET `/reports/patient/{id}` ← full patient history |

---

## Database Schema (Tables)

```
departments → doctors → appointments
                     ↗
patients ──────────────→ medical_records → prescriptions
         └─────────────→ lab_tests
         └─────────────→ bills
```

### Tables
- `departments` — Hospital departments
- `doctors` — Doctor profiles, linked to departments
- `patients` — Patient registration with demographics
- `appointments` — Scheduled visits (scheduled/completed/cancelled)
- `medical_records` — Treatment history per visit (diagnosis, treatment)
- `prescriptions` — Medications linked to records
- `lab_tests` — Ordered tests with results
- `bills` — Billing with payment status

---

## Team Members
- Milind Krishnan – RA2411026020367
- Allen Premji John – RA2411026020364
- Avinasha Ragavendra – RA2411026020323

**Supervisor:** Dr. Mohan M, Asst. Professor, Dept. of CSE-AIML
