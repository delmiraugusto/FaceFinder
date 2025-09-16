from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
import datetime
from .Base import Base
import uuid

class Reserva(Base):
    __tablename__ = 'reserva'
    
    codigo_uuid = Column(String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    numero_reserva = Column(String(50), nullable=False)
    status = Column(bool)
    data_checkin = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # hospede_id = Column(Integer, ForeignKey('hospede.id'), nullable=False)
    def __init__(self, numero_reserva, status, data_checkout, quarto_id):
        self.numero_reserva = numero_reserva
        self.status = status