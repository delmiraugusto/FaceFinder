from sqlalchemy import Table, Column, ForeignKey
from src.models.Base import Base

hospede_attempt = Table(
    'hospede_attempt',
    Base.metadata,
    Column('hospede_uuid', ForeignKey('hospede.codigo_uuid'), primary_key=True),
    Column('attempt_uuid', ForeignKey('attempt.codigo_uuid'), primary_key=True)
)
