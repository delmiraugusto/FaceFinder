from sqlalchemy.orm import Session
from src.models.DocumentData import DocumentData
from src.repository.documentData_repository import DocumentDataRepository
from src.service.attempt_service import AttemptService

class DocumentDataService:
    def __init__(self, session: Session):
        self.repo = DocumentDataRepository(session)
        self.attemp = AttemptService(session)
        self.session = session

    def criar_documentData(self, data, attempt_id):

        documentData = DocumentData(
        )

        self.attemp.listar_attempt(attempt_id)

        return self.repo.add(documentData, attempt_id)
    
    def listar_documentData(self, documentData_id):

        if documentData_id is None:
            raise ValueError("Codigo da documentData é obrigatório")
        
        documentData = self.repo.listar_documentData(documentData_id)

        if documentData is None:
            raise ValueError("DocumentData nao encontrada")
        
        return documentData
    
    def deletar_documentData(self, documentData_id):
        documentData = self.listar_documentData(documentData_id)

        return self.repo.deletar_documentData(documentData)
    
    def atualizar_documentData_parcial(self, documentData_id, data: dict):
        documentData = self.listar_documentData(documentData_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")

        return self.repo.update_patch_documentData(documentData, data)
    
    def atualizar_documentData_total(self, documentData_id, data: dict):
        documentData = self.listar_documentData(documentData_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")
        
        required_fields = ["status"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"O campo {field} é obrigatório para atualização")

        return self.repo.update_put_documentData(documentData, data) 