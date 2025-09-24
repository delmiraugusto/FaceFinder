from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.models.Base import Base
from src.models.Hospede_Attempt import hospede_attempt
import uuid

class Attempt(Base):
    __tablename__ = 'attempt'

    codigo_uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Boolean)

    hospedes = relationship(
        "Hospede",
        secondary=hospede_attempt,
        back_populates="attempts"
    )

    def __init__(self, status):
        self.status = status
