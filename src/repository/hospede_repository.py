from sqlalchemy.orm import Session

class HospedeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, hospede):
        self.session.add(hospede)
        self.session.commit()
        self.session.refresh(hospede)

        return hospede