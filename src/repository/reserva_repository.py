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
    
    def listar_reserva(self, reserva_id):
        return self.session.query(Reserva).filter_by(codigo_uuid=reserva_id).first()
    
    def deletar_reserva(self, reserva):
        self.session.delete(reserva)
        self.session.commit()
        return True

    def update_patch_reserva(self, reserva, data: dict):
        for key, value in data.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)

        self.session.commit()

        return reserva
    
    def update_put_reserva(self, reserva, data: dict):

        for key, value in data.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)

        self.session.commit()

        return reserva
    
    def forcar_status_reserva(self, reserva):
        self.session.merge(reserva)
        self.session.commit()
        return reserva

    def add_hospede(self, reserva_id, hospede_id):
        reserva = self.session.query(Reserva).get(reserva_id)
        hospede = self.session.query(Hospede).get(hospede_id)
        reserva.hospedes.append(hospede)
        self.session.commit()

        return reserva
    
