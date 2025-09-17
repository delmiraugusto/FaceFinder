from sqlalchemy.orm import Session
from src.models.Reserva import Reserva
from src.models.Hospede import Hospede

class ReservaRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, reserva):
        self.session.add(reserva)
        self.session.commit()
        self.session.refresh(reserva)
        return reserva
    
    def add_hospede(self, reserva_id, hospede_id):
        reserva = self.session.query(Reserva).get(reserva_id)
        hospede = self.session.query(Hospede).get(hospede_id)
        reserva.hospedes.append(hospede)
        self.session.commit()
        
        return reserva