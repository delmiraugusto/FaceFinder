import re
import sqlalchemy
from sqlalchemy.orm import Session
from src.models.Attempt import Attempt
from src.repository.attempt_repository import AttemptRepository
from src.service.hospede_service import HospedeService
from src.service.verificacao_service import verify_faces
from src.service.documentData_service import DocumentDataService
from src.models.Hospede_Attempt import hospede_attempt

class AttemptService:
    def __init__(self, session: Session):
        self.repo = AttemptRepository(session)
        self.hosp = HospedeService(session)
        self.doc = DocumentDataService(session)
        self.session = session

    def criar_attempt(self, data, hospede_id):

        hospede = self.hosp.listar_hospede(hospede_id)

        document_base64 = data.get("document")
        selfie_base64 = data.get("selfie")

        resultadoVerify = verify_faces(document_base64, selfie_base64)

        attempt = Attempt(
            status=resultadoVerify["verification"]["verified"]
        )

        tentativas_invalidas_hoje = self.repo.contar_attempts_invalidas_hoje(hospede_id)

        if  tentativas_invalidas_hoje >= 3:
            raise ValueError("Limite de tentativas inválidas atingidas por hoje.")
        
        status = attempt.status
        
        self.hosp.forcar_status_hospede(hospede_id, status)
        
        tentativas_restantes = 3 - tentativas_invalidas_hoje

        attempt = self.repo.add(attempt, hospede_id)

        document_data_json = resultadoVerify["document_data"]

        self.doc.criar_documentData(document_data_json, attempt.codigo_uuid)

        return {
            "verification": resultadoVerify["verification"],
            "document_data": resultadoVerify["document_data"],
            "faces": resultadoVerify["faces"],
            "attempt": attempt,
            "tentativas_invalidas_restantes": max(tentativas_restantes, 0)
        }

    
    def listar_attempt(self, attempt_id):

        if attempt_id is None:
            raise ValueError("Codigo da attempt é obrigatório")
        
        attempt = self.repo.listar_attempt(attempt_id)

        if attempt is None:
            raise ValueError("Attempt nao encontrada")
        
        return attempt
    
    def deletar_attempt(self, attempt_id):
        attempt = self.listar_attempt(attempt_id)

        return self.repo.deletar_attempt(attempt)
    
    def atualizar_attempt_parcial(self, attempt_id, data: dict):
        attempt = self.listar_attempt(attempt_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")

        return self.repo.update_patch_attempt(attempt, data)
    
    def atualizar_attempt_total(self, attempt_id, data: dict):
        attempt = self.listar_attempt(attempt_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")
        
        required_fields = ["status"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"O campo {field} é obrigatório para atualização")

        return self.repo.update_put_attempt(attempt, data) 
    
    def forcar_status_attempt(self, attempt_id, status):
        attempt = self.listar_attempt(attempt_id)

        attempt.status = status
        
        return self.repo.forcar_status_attempt(attempt)
    
    def remover_hospede_da_attempt(self, attempt_id, hospede_id):

        attempt = self.listar_attempt(attempt_id)
        
        hospede = next((h for h in attempt.hospedes if h.codigo_uuid == hospede_id), None)

        if hospede is None:
            raise ValueError("Hospede nao encontrado na attempt")
        
        return self.repo.deletar_hospede_da_attempt(attempt, hospede)
