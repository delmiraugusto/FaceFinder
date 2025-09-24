from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from src.models.Base import Base
from src.models.Hospede_Attempt import hospede_attempt
from src.models.Hospede_Reserva import hospede_reserva
import uuid

class Hospede(Base):
    __tablename__ = 'hospede'

    codigo_uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Boolean)

    reservas = relationship(
        "Reserva",
        secondary=hospede_reserva,
        back_populates="hospedes"
    )

    attempts = relationship(
        "Attempt",
        secondary=hospede_attempt,
        back_populates="hospedes"
    )

    def __init__(self, status=None):
        self.status = status
