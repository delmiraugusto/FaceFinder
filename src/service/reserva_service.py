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


    def adicionar_hospede_a_reserva(self, reserva_id, hospede_id):
        return self.repo.add_hospede(reserva_id, hospede_id)
