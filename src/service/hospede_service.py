from sqlalchemy.orm import Session
from src.repository.hospede_repository import HospedeRepository
from src.models.Hospede import Hospede
from src.schemas.HospedeSchema import HospedeUpdateSchema

class HospedeService:
    def __init__(self, session: Session):
        self.repo = HospedeRepository(session)
        self.session = session

    def criar_hospede(self, data):
        
        hospede = Hospede(**data)

        return self.repo.add(hospede)
    
    def listar_hospede(self, hospede_id):

        if hospede_id is None:
            raise ValueError("Codigo do hospede é obrigatório")
        
        hospede = self.repo.listar_hospede(hospede_id)

        if hospede is None:
            raise ValueError("Hospede nao encontrado")
        
        return hospede
    
    def deletar_hospede(self, hospede_id):
        hospede = self.listar_hospede(hospede_id)

        return self.repo.deletar_hospede(hospede)
    
    def atualizar_hospede_parcial(self, hospede_id, data: dict):
        hospede = self.listar_hospede(hospede_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")

        return self.repo.update_patch_hospede(hospede, data)
    
    def atualizar_hospede_total(self, hospede_id, data: dict):
        hospede = self.listar_hospede(hospede_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")
        
        schema = HospedeUpdateSchema()
        
        errors = schema.validate(data)
        if errors:
            raise ValueError(f"Erros de validação: {errors}")

        return self.repo.update_put_hospede(hospede, data)
    
    def forcar_status_hospede(self, hospede_id, status):
        hospede = self.listar_hospede(hospede_id)

        hospede.status = status
        
        return self.repo.forcar_status_hospede(hospede)

