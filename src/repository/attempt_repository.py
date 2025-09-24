from sqlalchemy.orm import Session
from src.models.Attempt import Attempt
from src.models.Hospede import Hospede

class AttemptRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, attempt, hospede_id):
        self.session.add(attempt)
        self.session.commit()
        self.session.refresh(attempt)

        attempt_id = attempt.codigo_uuid

        attempt = self.session.query(Attempt).get(attempt_id)
        hospede = self.session.query(Hospede).get(hospede_id)
        attempt.hospedes.append(hospede)
        self.session.commit()

        return attempt

    
    def listar_attempt(self, attempt_id):
        return self.session.query(Attempt).filter_by(codigo_uuid=attempt_id).first()
    
    def deletar_attempt(self, attempt):
        self.session.delete(attempt)
        self.session.commit()
        return True

    def update_patch_attempt(self, attempt, data: dict):
        for key, value in data.items():
            if hasattr(attempt, key):
                setattr(attempt, key, value)

        self.session.commit()

        return attempt
    
    def update_put_attempt(self, attempt, data: dict):

        for key, value in data.items():
            if hasattr(attempt, key):
                setattr(attempt, key, value)

        self.session.commit()

        return attempt
    
    def forcar_status_attempt(self, attempt):
        self.session.merge(attempt)
        self.session.commit()
        return attempt
    
    def deletar_hospede_da_attempt(self, attempt, hospede):
        if hospede in attempt.hospedes:
            attempt.hospedes.remove(hospede)
            self.session.commit()
        return True
    
