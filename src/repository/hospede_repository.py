from sqlalchemy.orm import Session
from src.models.Hospede import Hospede

class HospedeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, hospede):
        self.session.add(hospede)
        self.session.commit()
        self.session.refresh(hospede)

        return hospede
    
    def listar_hospede(self, hospede_id):
        return self.session.query(Hospede).filter_by(codigo_uuid=hospede_id).first()
    
    def deletar_hospede(self, hospede):
        self.session.delete(hospede)
        self.session.commit()
        return True

    def update_patch_hospede(self, hospede, data: dict):
        for key, value in data.items():
            if hasattr(hospede, key):
                setattr(hospede, key, value)

        self.session.commit()

        return hospede
    
    def update_put_hospede(self, hospede, data: dict):

        for key, value in data.items():
            if hasattr(hospede, key):
                setattr(hospede, key, value)

        self.session.commit()

        return hospede
    
    def forcar_status_hospede(self, hospede):
        self.session.merge(hospede)
        self.session.commit()
        return hospede