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


    def adicionar_hospede_a_reserva(self, reserva_id, hospede_id):

        if reserva_id is None or hospede_id is None:
            raise ValueError("Codigo da reserva e do hospede sao obrigatorios")
        
        return self.repo.add_hospede(reserva_id, hospede_id)
