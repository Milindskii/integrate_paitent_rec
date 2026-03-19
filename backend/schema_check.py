from database import engine
from sqlalchemy import text

def find_doctors_schema():
    print(f"Checking engine: {engine.url}")
    with engine.connect() as conn:
        try:
            # Check all schemas for the doctors table
            query = text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'doctors'")
            results = conn.execute(query).all()
            if not results:
                print("ABSOLUTE FAILURE: 'doctors' table not found in ANY schema.")
            else:
                for schema, name in results:
                    print(f"FOUND: Table '{name}' in schema '{schema}'")
                    
            # Check current search path
            path = conn.execute(text("SHOW search_path")).scalar()
            print(f"Current search_path: {path}")
            
        except Exception as e:
            print(f"DIAGNOSTIC ERROR: {e}")

if __name__ == "__main__":
    find_doctors_schema()
