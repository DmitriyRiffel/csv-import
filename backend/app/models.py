from sqlalchemy import Column, Integer, String, Date
from database import Base

class Contract(Base):
    __tablename__ = 'contracts' 
    id = Column(Integer, primary_key=True, index=True)

    contract_number = Column(String, unique=True, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    status = Column(String, nullable=False)