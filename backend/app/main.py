import tempfile
from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlalchemy.orm import Session
from app.services.contract_import import validate_csv_file
from app.schemas.contract import ContractResponse
from .models import Contract
from .database import Base, engine, SessionLocal
import shutil

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/testcheck")
def test_check():
    """
    Simple check endpoint to verify that the API is running.
    """
    return {"status": "ok"}

@app.get("/contracts", response_model=list[ContractResponse])
def get_contracts(db: Session = Depends(get_db)):
    """
    Return all contracts stored in the database.
    """
    # Select * FROM contracts;
    contracts = db.query(Contract).all()
    return contracts

@app.delete("/contracts")
def delete_contracts(db: Session = Depends(get_db)):
    """
    Delete all contracts from the database
    """
    db.query(Contract).delete()
    db.commit()
    return {"success": True, "message": "Alle Verträge gelöscht"}

@app.post("/contracts/upload")
async def upload_contracts_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    """
    Upload a CSV file with contracts, validate it an import valid rows into the database.
    Returns information about success, imported rows and errors.
    """
    # Basic file type check. Only allow files with .csv extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Nur .csv Dateien sind erlaubt")
    
    # Write the uploaded file into a temporary file on disk
    # so you can pass a normal filesystem path to the validator function.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp_path = Path(tmp.name)
        # Copy the content of the uploaded file stream into the temp file.
        shutil.copyfileobj(file.file, tmp)

    try:
        # Validate the CSV file and collect valid rows and errors. 
        valid_rows, errors = validate_csv_file(tmp_path)

        # Load all existing contract numbers from the database into a set
        # to efficiently check for duplicates.
        existing = {
            c.contract_number
            for c in db.query(Contract.contract_number).all()
        }

        # Counter for succesfully inserted contracts.
        imported_count = 0

        # Amount for not inserted contracts.
        not_imported_amount = 0

        # Insert each valid row into the database if the contract number is not a duplicate.
        for c in valid_rows:
            # Check if this contract number already exists in the database.
            if c.contract_number in existing:
                # Add a dublicate error and skip this row
                errors.append({
                    "line": None,
                    "contract_number": c.contract_number,
                    "error": f"Vertragsnummer {c.contract_number} existiert bereits",
                })
                continue

            # Create a new Contract ORM object from the validated Pydantic model .
            db_contract = Contract(
                contract_number=c.contract_number,
                start_date=c.start_date,
                end_date=c.end_date,
                status=c.status,
            )
            # Stage the new contract for insertion
            db.add(db_contract)
            imported_count += 1

            # Add this contract number to the existing set
            # so duplicates within the same file are also detected.
            existing.add(c.contract_number)

        not_imported_amount = len(valid_rows) - imported_count

        # Commit all staged inserts in one transaction.
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Fehler beim Speichern."
            )

        # If there were any errors, report error and the number of imported rows if there are any.
        if errors: 
            return {
                "success": False,
                "imported": imported_count,
                "not_imported": not_imported_amount,
                "errors": errors,
            }
        
        # If there are no errors, report success and the number of imported rows.
        return {
            "success": True,
            "imported": imported_count,
            "not_imported": not_imported_amount,
            "errors": [],
        }
    finally:
        try: 
            tmp_path.unlink()
        except FileNotFoundError: 
            pass
    

