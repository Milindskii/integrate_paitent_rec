from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine
import models
from routes import patients, admin_routes, reports
import traceback

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MediSync API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     print(f"GLOBAL ERROR: {str(exc)}")
#     traceback.print_exc()
#     return JSONResponse(
#         status_code=500,
#         content={"detail": str(exc), "traceback": traceback.format_exc()},
#     )

# Include routers
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(admin_routes.router, prefix="/api", tags=["Admin"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


@app.get("/")
def root():
    return {"message": "MediSync API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}