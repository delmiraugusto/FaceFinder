from sqlalchemy import Table, Column, ForeignKey
from .Base import Base

hospede_reserva = Table(
    'hospede_reserva',
    Base.metadata,
    Column('hospede_id', ForeignKey('hospede.id'), primary_key=True),
    Column('reserva_id', ForeignKey('reserva.id'), primary_key=True)
)
