from sqlalchemy import Table, Column, ForeignKey
from src.models.Base import Base

hospede_reserva = Table(
    'hospede_reserva',
    Base.metadata,
    Column('hospede_uuid', ForeignKey('hospede.codigo_uuid'), primary_key=True),
    Column('reserva_uuid', ForeignKey('reserva.codigo_uuid'), primary_key=True)
)
