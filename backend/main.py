from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import patients, admin_routes, reports

# Create all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediSync API", version="1.0.0")

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ───────────────────────────────────────────────────────────────────
app.include_router(patients.router,     prefix="/api/patients",  tags=["Patients"])
app.include_router(admin_routes.router, prefix="/api",           tags=["Admin"])
app.include_router(reports.router,      prefix="/api/reports",   tags=["Reports"])


@app.get("/")
def root():
    return {"message": "MediSync API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}