from sqlalchemy.orm import Session
from src.repository.hospede_repository import HospedeRepository
from src.models.Hospede import Hospede

class HospedeService:
    def __init__(self, session: Session):
        self.repo = HospedeRepository(session)
        self.session = session

    def criar_hospede(self, data):

        hospede = Hospede(
            status=data.get("status")
        )

        return self.repo.add(hospede)

