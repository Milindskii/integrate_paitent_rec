from database import engine, SessionLocal, Base
import models
from models import Department

def force_refresh():
    print(f"Connecting to: {engine.url}")
    print("DROPPING ALL TABLES...")
    Base.metadata.drop_all(bind=engine)
    print("CREATING ALL TABLES...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Adding General department...")
        gen = Department(name='General', description='General Department')
        db.add(gen)
        db.commit()
        print("General department added.")
        
        from sqlalchemy import text
        res = db.execute(text("SELECT COUNT(*) FROM doctors")).scalar()
        print(f"Current doctor count: {res}")
        
    except Exception as e:
        print(f"REFRESH ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    force_refresh()
