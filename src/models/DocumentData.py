from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.models.Base import Base
from src.models.Attempt_DocumentData import attempt_documentData
from sqlalchemy.dialects.postgresql import JSONB
import uuid

class DocumentData(Base):
    __tablename__ = 'documentdata'

    codigo_uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dados = Column(JSONB)

    attempts = relationship(
        "Attempt",
        secondary=attempt_documentData,
        back_populates="documentDatas"
    )

    def __init__(self, dados):
        self.dados = dados
