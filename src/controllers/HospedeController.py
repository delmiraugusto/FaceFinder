from flask import request
from flask_restful import Resource
from src.models.Base import db
from src.service.hospede_service import HospedeService

class HospedeResource(Resource):

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
        
class HospedeListResource(Resource):
        
    def get(self, hospede_id):
        hospede_service = HospedeService(db.session)
        try:
            hospede = hospede_service.listar_hospede(hospede_id)

            return {
                "codigo_uuid": hospede.codigo_uuid,
                "status": str(hospede.status),
                "reservas": [
                    {
                        "codigo_uuid": reserva.codigo_uuid,
                        "status": bool(reserva.status)
                    }
                    for reserva in hospede.reservas
                ]
            }, 200
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
        try:
            data = request.get_json()
            hospede = hospede_service.atualizar_hospede_parcial(hospede_id, data)
            return {
                "codigo_uuid": hospede.codigo_uuid,
                "status": str(hospede.status),
                "reservas": [
                    {
                        "codigo_uuid": reserva.codigo_uuid,
                        "status": bool(reserva.status)
                    }
                    for reserva in hospede.reservas
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
    

    def put(self, hospede_id):
        hospede_service = HospedeService(db.session)
        try:
            data = request.get_json()
            hospede = hospede_service.atualizar_hospede_total(hospede_id, data)
            return {
                "codigo_uuid": hospede.codigo_uuid,
                "status": str(hospede.status),
                "reservas": [
                    {
                        "codigo_uuid": reserva.codigo_uuid,
                        "status": bool(reserva.status)
                    }
                    for reserva in hospede.reservas
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
class HospedeStatusResource(Resource):

    def patch(self, hospede_id):
        hospede_service = HospedeService(db.session)
        try:
            hospede = hospede_service.forcar_status_hospede(hospede_id)
            return {
                "codigo_uuid": hospede.codigo_uuid,
                "status": str(hospede.status),
                "reservas": [
                    {
                        "codigo_uuid": reserva.codigo_uuid,
                        "status": bool(reserva.status)
                    }
                    for reserva in hospede.reservas
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
    