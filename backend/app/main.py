import tempfile
from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlalchemy import false
from sqlalchemy.orm import Session
from app.services.contract_import import validate_csv_file
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
def test_cheack():
    return {"status": "ok"}

@app.get("/contracts")
def list_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return contracts

@app.delete("/contracts")
def clear_contracts(db: Session = Depends(get_db)):
    db.query(Contract).delete()
    db.commit()
    return {"success": True, "message": "Alle Verträge gelöscht"}

@app.post("/contracts/upload")
async def upload_contracts_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Nur .csv Dateien sind erlaubt")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp_path = Path(tmp.name)
        shutil.copyfileobj(file.file, tmp)

    valid_rows, errors = validate_csv_file(tmp_path)

    if errors: 
        return {
            "success": False,
            "imported": 0,
            "errors": errors,
        }
    
    for c in valid_rows:
        db_contract = Contract(
            contract_number=c.contract_number,
            start_date=c.start_date,
            end_date=c.end_date,
            status=c.status,
        )
        db.add(db_contract)

    db.commit()
    
    return {
        "success": True,
        "imported": len(valid_rows),
        "errors": [],
    }
    

