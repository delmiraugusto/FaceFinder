from flask import request
from flask_restful import Resource
from src.models.Base import db
from src.service.hospede_service import HospedeService

class HospedeListResource(Resource):

    def post(self):
        hospede_service = HospedeService(db.session)
        try:
            data = request.get_json()
            hospede = hospede_service.criar_hospede(data)
            return {
                "codigo_uuid": hospede.codigo_uuid,
                "status": str(hospede.status),
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
    