import re
from src.models.Reserva import Reserva
from src.repository.reserva_repository import ReservaRepository
from sqlalchemy.orm import Session

class ReservaService:
    def __init__(self, session: Session):
        self.repo = ReservaRepository(session)
        self.session = session

    def criar_reserva(self, data):

        reserva = Reserva(
            numero_reserva=data.get("numero_reserva"),
            status=data.get("status")
        )

        return self.repo.add(reserva)
    
    def listar_reserva(self, reserva_id):

        if reserva_id is None:
            raise ValueError("Codigo da reserva é obrigatório")
        
        reserva = self.repo.listar_reserva(reserva_id)

        if reserva is None:
            raise ValueError("Reserva nao encontrada")
        
        return reserva
    
    def deletar_reserva(self, reserva_id):
        reserva = self.listar_reserva(reserva_id)

        return self.repo.deletar_reserva(reserva)
    
    def atualizar_reserva_parcial(self, reserva_id, data: dict):
        reserva = self.listar_reserva(reserva_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")

        return self.repo.update_patch_reserva(reserva, data)
    
    def atualizar_reserva_total(self, reserva_id, data: dict):
        reserva = self.listar_reserva(reserva_id)

        if not data:
            raise ValueError("Nenhum dado fornecido para atualizar")
        
        required_fields = ["numero_reserva", "status"]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"O campo {field} é obrigatório para atualização")

        return self.repo.update_put_reserva(reserva, data)
    
    def forcar_status_reserva(self, reserva_id, status):
        reserva = self.listar_reserva(reserva_id)

        reserva.status = status
        
        return self.repo.forcar_status_reserva(reserva)


    def adicionar_hospede_a_reserva(self, reserva_id, hospede_id):

        reserva = self.listar_reserva(reserva_id)

        if reserva_id is None or hospede_id is None:
            raise ValueError("Codigo da reserva e do hospede sao obrigatorios")
        
        ja_existe = any(h.codigo_uuid == hospede_id for h in reserva.hospedes)
        if ja_existe:
            raise ValueError("Hospede já está cadastrado nesta reserva")
        
        return self.repo.add_hospede(reserva_id, hospede_id)
    
    def remover_hospede_da_reserva(self, reserva_id, hospede_id):

        reserva = self.listar_reserva(reserva_id)
        
        hospede = next((h for h in reserva.hospedes if h.codigo_uuid == hospede_id), None)

        if hospede is None:
            raise ValueError("Hospede nao encontrado na reserva")
        
        return self.repo.deletar_hospede_da_reserva(reserva, hospede)
