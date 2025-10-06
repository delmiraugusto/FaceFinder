from sqlalchemy import Table, Column, ForeignKey
from src.models.Base import Base

attempt_documentData = Table(
    'attempt_documentData',
    Base.metadata,
    Column('documentData_uuid', ForeignKey('documentData.codigo_uuid'), primary_key=True),
    Column('attempt_uuid', ForeignKey('attempt.codigo_uuid'), primary_key=True)
)
