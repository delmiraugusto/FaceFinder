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
    nome = Column(String(100))
    ag_uid = Column(String(36))

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

    def __init__(self, nome=None, status=None, ag_uid=None):
        self.nome = nome
        self.status = status
        self.ag_uid = ag_uid