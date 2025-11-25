from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional

class ContractCSV(BaseModel):
    contract_number : str
    start_date: date
    end_date: Optional[date] = None
    status: str

    @field_validator("status")
    def validate_status(cls, value):
        allowed = {"aktiv", "gekündigt", "abgelaufen"}
        if value not in allowed: 
            raise ValueError(f"Ungültiger Status: {value}. Erlaubt: {allowed}")
        return value
    
    @field_validator("end_date")
    def validate_dates(cls, value, info):
        start_date = info.data.get("start_date") 
        if value and start_date and value < start_date:
            raise ValueError("end_date darf nicht vor start_date liegen")
        return value