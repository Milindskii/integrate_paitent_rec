from database import engine, SessionLocal
from sqlalchemy import text
import models

def debug_doctors():
    db = SessionLocal()
    try:
        # Check departments first
        depts = db.execute(text("SELECT id, name FROM departments")).all()
        print(f"Departments in DB: {depts}")
        
        # Check doctors raw
        docs = db.execute(text("SELECT id, name, email FROM doctors WHERE is_active = True")).all()
        print(f"Raw doctors count: {len(docs)}")
        
        # Check SQLAlchemy query
        from models import Doctor
        query_docs = db.query(Doctor).filter(Doctor.is_active == True).all()
        print(f"SQLAlchemy doctors count: {len(query_docs)}")
        
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_doctors()
