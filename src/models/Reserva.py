from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.models.Base import Base
from src.models.Hospede_Reserva import hospede_reserva
import datetime, uuid

class Reserva(Base):
    __tablename__ = 'reserva'

    codigo_uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    numero_reserva = Column(String(50), nullable=False)
    status = Column(Boolean)
    data_checkin = Column(DateTime, default=datetime.datetime.now)

    hospedes = relationship(
        "Hospede",
        secondary=hospede_reserva,
        back_populates="reservas"
    )

    def __init__(self, numero_reserva, status):
        self.numero_reserva = numero_reserva
        self.status = status
