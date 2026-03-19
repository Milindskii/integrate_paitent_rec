from database import engine, SessionLocal, Base
import models
from models import Department

def full_init():
    print(f"Connecting to: {engine.url}")
    print("Dropping all tables (cleanup)...")
    # Base.metadata.drop_all(bind=engine) # Safer to just create if not exists for now
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if General exists
        gen = db.query(Department).filter(Department.name == 'General').first()
        if not gen:
            print("Adding General department...")
            gen = Department(name='General', description='General Department')
            db.add(gen)
            db.commit()
            print("General department added.")
        else:
            print("General department already exists.")
            
        # Verify doctors table
        from sqlalchemy import text
        res = db.execute(text("SELECT COUNT(*) FROM doctors")).scalar()
        print(f"Current doctor count: {res}")
        
    except Exception as e:
        print(f"INIT ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    full_init()
