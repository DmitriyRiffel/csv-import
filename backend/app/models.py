from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Contract(Base):
    __tablename__ = 'contracts' 
    contract_number = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String, nullable=False)