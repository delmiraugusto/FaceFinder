from flask import request
from flask_restful import Resource
import os
from src.service.attempt_service import AttemptService
from src.models.Base import db
from src.config.auth import require_api_key
from src.models.Attempt import Attempt
from src.schemas.AttemptSchema import AttemptSchema

ATTEMPT_API_KEY = os.getenv("ATTEMPT_API_KEY")

class AttemptBaseResource(Resource):
    method_decorators = [require_api_key(ATTEMPT_API_KEY)]

class AttemptResource(AttemptBaseResource):
    def post(self, hospede_id, reserva_id):
        attempt_service = AttemptService(db.session)
        schema = AttemptSchema(exclude=("hospedes",))
        try:
            data = request.get_json()

            resultado = attempt_service.criar_attempt(data, hospede_id, reserva_id)

            attempt_serialized = schema.dump(resultado["attempt"])
            
            return {
                "attempt": attempt_serialized,
                "verification": resultado["verification"],
                "document_data": resultado["document_data"],
                "faces": resultado["faces"]
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class AttemptListResource(AttemptBaseResource):
        
    def get(self, attempt_id):
        attempt_service = AttemptService(db.session)
        try:
            attempt = attempt_service.listar_attempt(attempt_id)
            return {
                "codigo_uuid": attempt.codigo_uuid,
                "status": str(attempt.status),
                "create_at": attempt.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in attempt.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, attempt_id):
        attempt_service = AttemptService(db.session)
        try:
            attempt_service.deletar_attempt(attempt_id)
            
            return '', 204
            
        except Exception as e:
            return {"error": str(e)}, 400
    
    def patch(self, attempt_id):
        attempt_service = AttemptService(db.session)
        try:
            data = request.get_json()
            attempt = attempt_service.atualizar_attempt_parcial(attempt_id, data)
            return {
                "codigo_uuid": attempt.codigo_uuid,
                "status": str(attempt.status),
                "create_at": attempt.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in attempt.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
    
    def put(self, attempt_id):
        attempt_service = AttemptService(db.session)
        try:
            data = request.get_json()
            attempt = attempt_service.atualizar_attempt_total(attempt_id, data)
            return {
                "codigo_uuid": attempt.codigo_uuid,
                "status": str(attempt.status),
                "create_at": attempt.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in attempt.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
class AttemptStatusResource(AttemptBaseResource):

    def patch(self, attempt_id):
        attempt_service = AttemptService(db.session)
        data = request.get_json()
        try:
            attempt = attempt_service.forcar_status_attempt(attempt_id, data['status'])
            return {
                "codigo_uuid": attempt.codigo_uuid,
                "status": str(attempt.status),
                "create_at": attempt.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in attempt.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400