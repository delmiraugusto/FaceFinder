import re
from sqlalchemy.orm import Session
from src.models.Attempt import Attempt
from src.repository.attempt_repository import AttemptRepository
from src.service.hospede_service import HospedeService

class AttemptService:
    def __init__(self, session: Session):
        self.repo = AttemptRepository(session)
        self.hosp = HospedeService(session)
        self.session = session

    def criar_attempt(self, data, hospede_id):

        attempt = Attempt(
            status=data.get("status")
        )

        self.hosp.listar_hospede(hospede_id)

        return self.repo.add(attempt, hospede_id)
    
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
