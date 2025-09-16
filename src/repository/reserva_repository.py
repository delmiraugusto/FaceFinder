from src.models.Reserva import Reserva
from sqlalchemy.orm import Session

class ReservaRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, reserva):
        self.session.add(reserva)
        self.session.commit()
        self.session.refresh(reserva)
        return reserva