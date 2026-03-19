from database import engine, SessionLocal
from sqlalchemy import text
from models import Doctor

def debug_sqlalchemy_model():
    db = SessionLocal()
    try:
        # Get the table name from the model
        table_name = Doctor.__table__.name
        print(f"SQLAlchemy model 'Doctor' expects table: {table_name}")
        
        # Try raw SQL on that table
        res = db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        print(f"Raw SQL count on {table_name}: {res}")
        
        # Try SQLAlchemy query
        count = db.query(Doctor).count()
        print(f"SQLAlchemy query count: {count}")
    except Exception as e:
        print(f"DETAIL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_sqlalchemy_model()
