from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime
from src.models.Hospede_Reserva import hospede_reserva
from .Base import Base
import uuid

class Reserva(Base):
    __tablename__ = 'reserva'
    
    codigo_uuid = Column(String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    numero_reserva = Column(String(50), nullable=False)
    status = Column(Boolean)
    data_checkin = Column(DateTime, nullable=False, default=datetime.datetime.now)

    hospedes = relationship("Hospede", secondary=hospede_reserva, back_populates="reservas")

    def __init__(self, numero_reserva, status, hospede_id):
        self.numero_reserva = numero_reserva
        self.status = status
        self.hospede_id = hospede_id