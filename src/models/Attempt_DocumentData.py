from sqlalchemy import Table, Column, ForeignKey
from src.models.Base import Base

attempt_documentData = Table(
    'attempt_documentdata',
    Base.metadata,
    Column('documentdata_uuid', ForeignKey('documentdata.codigo_uuid'), primary_key=True),
    Column('attempt_uuid', ForeignKey('attempt.codigo_uuid'), primary_key=True)
)
