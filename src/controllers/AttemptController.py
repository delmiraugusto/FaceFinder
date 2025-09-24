from flask import request
from flask_restful import Resource
import os
from src.service.attempt_service import AttemptService
from src.models.Base import db
from src.config.auth import require_api_key

ATTEMPT_API_KEY = os.getenv("ATTEMPT_API_KEY")

class AttemptBaseResource(Resource):
    method_decorators = [require_api_key(ATTEMPT_API_KEY)]

class AttemptResource(AttemptBaseResource):
    def post(self, hospede_id):
        attempt_service = AttemptService(db.session)
        try:
            data = request.get_json()
            attempt = attempt_service.criar_attempt(data, hospede_id)
            return {
                "codigo_uuid": attempt.codigo_uuid,
                "status": str(attempt.status),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in attempt.hospedes
                ]
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
    