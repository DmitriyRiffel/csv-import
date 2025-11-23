from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    contracts = db.query(models.Contract).all()
    return contracts

