from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import patients, doctors, admin, admin_routes, reports, appointments

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediSync API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(patients.router,      prefix="/api/patients",      tags=["Patients"])
app.include_router(doctors.router,       prefix="/api/doctors",       tags=["Doctors"])
app.include_router(admin.router,         prefix="/api/admin",         tags=["Admin"])
app.include_router(appointments.router,  prefix="/api/appointments",  tags=["Appointments"])
app.include_router(reports.router,       prefix="/api/reports",       tags=["Reports"])
app.include_router(admin_routes.router,  prefix="/api",               tags=["Admin Routes"])


@app.get("/")
def root():
    return {"message": "MediSync API v2.0 is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}