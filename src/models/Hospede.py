from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.models.Hospede_Reserva import hospede_reserva
from .Base import Base
import uuid

class Hospede(Base):
    __tablename__ = 'hospede'

    codigo_uuid = Column(String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    status = Column(Boolean)

    reservas = relationship("Reserva", secondary=hospede_reserva, back_populates="hospedes")

    def __init__(self, status):
        self.status = status