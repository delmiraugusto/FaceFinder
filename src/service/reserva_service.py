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
        
        return self.repo.listar_reserva(reserva_id)
    
    def atualizar_reserva(self, reserva_id, data):
        reserva = self.repo.listar_reserva(reserva_id)
        if not reserva:
            raise ValueError("Reserva not found")

        if "numero_reserva" in data:
            reserva.numero_reserva = data["numero_reserva"]
        if "status" in data:
            reserva.status = data["status"]

        self.session.commit()
        self.session.refresh(reserva)
        return reserva
    



    def adicionar_hospede_a_reserva(self, reserva_id, hospede_id):
        return self.repo.add_hospede(reserva_id, hospede_id)
