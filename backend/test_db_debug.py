from database import SessionLocal
import crud
import schemas

def test_get_doctors():
    db = SessionLocal()
    try:
        doctors = crud.get_doctors(db)
        print(f"Successfully fetched {len(doctors)} doctors")
        for d in doctors:
            # Try to validate with schema
            schemas.Doctor.model_validate(d)
        print("Schema validation successful")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_get_doctors()
