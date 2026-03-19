import psycopg2
import os

DATABASE_URL = "postgresql://postgres:milind7841@localhost:5432/patient_records_db"

def run_migration():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Add columns to doctors table
        print("Adding columns to doctors table...")
        cur.execute("ALTER TABLE doctors ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);")
        cur.execute("ALTER TABLE doctors ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;")
        
        # Add columns to patients table
        print("Adding columns to patients table...")
        cur.execute("ALTER TABLE patients ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;")
        
        conn.commit()
        cur.close()
        conn.close()
        print("Migration successful!")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
