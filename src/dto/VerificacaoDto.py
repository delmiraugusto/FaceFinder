from pydantic import BaseModel

class VerificacaoDto(BaseModel):

    document: str
    selfie: str
