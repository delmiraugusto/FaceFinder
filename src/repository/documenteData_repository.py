from sqlalchemy.orm import Session
from src.models.DocumentData import DocumentData
from src.models.Attempt import Attempt

class DocumentDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, documentData, attempt_id):
        self.session.add(documentData)
        self.session.commit()
        self.session.refresh(documentData)

        documentData_id = documentData.codigo_uuid

        documentData = self.session.query(DocumentData).get(documentData_id)
        attempt = self.session.query(Attempt).get(attempt_id)
        documentData.attempts.append(attempt)
        self.session.commit()

        return documentData
    
    def listar_documentData(self, documentData_id):
        return self.session.query(DocumentData).filter_by(codigo_uuid=documentData_id).first()
    
    def deletar_documentData(self, documentData):
        self.session.delete(documentData)
        self.session.commit()
        return True

    def update_patch_documentData(self, documentData, data: dict):
        for key, value in data.items():
            if hasattr(documentData, key):
                setattr(documentData, key, value)

        self.session.commit()

        return documentData
    
    def update_put_documentData(self, documentData, data: dict):

        for key, value in data.items():
            if hasattr(documentData, key):
                setattr(documentData, key, value)

        self.session.commit()

        return documentData