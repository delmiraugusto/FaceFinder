import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from src.models.Base import Base
from src.models.Hospede_Attempt import hospede_attempt
from src.models.Attempt_DocumentData import attempt_documentData
import uuid

class Attempt(Base):
    __tablename__ = 'attempt'

    codigo_uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Boolean)
    create_at = Column(DateTime, default=datetime.datetime.now)
    dia = Column(Date, default=datetime.date.today)    

    hospedes = relationship(
        "Hospede",
        secondary=hospede_attempt,
        back_populates="attempts"
    )

    documentDatas = relationship(
        "DocumentData",
        secondary=attempt_documentData,
        back_populates="attempts"
    )

    def __init__(self, status):
        self.status = status

