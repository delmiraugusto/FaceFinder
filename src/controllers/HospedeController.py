from flask import request
from flask_restful import Resource
import os
from src.models.Base import db
from src.service.hospede_service import HospedeService
from src.config.auth import require_api_key
from src.schemas.HospedeSchema import HospedeSchema

HOSPEDE_API_KEY = os.getenv("HOSPEDE_API_KEY")

class HospedeBaseResource(Resource):
    method_decorators = [require_api_key(HOSPEDE_API_KEY)]

class HospedeResource(HospedeBaseResource):

    def post(self):
        hospede_service = HospedeService(db.session)
        schema = HospedeSchema(exclude=("reservas", "attempts"))
        try:
            data = request.get_json()
            hospede = hospede_service.criar_hospede(data)
            return schema.dump(hospede), 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class HospedeListResource(HospedeBaseResource):
        
    def get(self, hospede_id):
        hospede_service = HospedeService(db.session)
        schema = HospedeSchema()
        try:
            hospede = hospede_service.listar_hospede(hospede_id)
            return schema.dump(hospede), 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, hospede_id):
        hospede_service = HospedeService(db.session)
        try:
            hospede_service.deletar_hospede(hospede_id)
            return '', 204
            
        except Exception as e:
            return {"error": str(e)}, 400
        
    def patch(self, hospede_id):
        hospede_service = HospedeService(db.session)
        schema = HospedeSchema(exclude=("reservas", "attempts"))
        try:
            data = request.get_json()
            hospede = hospede_service.atualizar_hospede_parcial(hospede_id, data)
            return schema.dump(hospede), 200
        except Exception as e:
            return {"error": str(e)}, 400
    

    def put(self, hospede_id):
        hospede_service = HospedeService(db.session)
        schema = HospedeSchema(exclude=("reservas", "attempts"))

        try:
            data = request.get_json()
            hospede = hospede_service.atualizar_hospede_total(hospede_id, data)
            return schema.dump(hospede), 200
        except Exception as e:
            return {"error": str(e)}, 400
        
class HospedeStatusResource(HospedeBaseResource):

    def patch(self, hospede_id):
        hospede_service = HospedeService(db.session)
        schema = HospedeSchema(exclude=("reservas", "attempts"))
        try:
            data = request.get_json()
            status = data.get("status")
            hospede = hospede_service.forcar_status_hospede(hospede_id, status)
            return schema.dump(hospede), 200
        except Exception as e:
            return {"error": str(e)}, 400
    