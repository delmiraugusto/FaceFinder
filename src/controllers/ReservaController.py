from flask import request
from flask_restful import Resource
from src.service.reserva_service import ReservaService
from src.models.Base import db

class ReservaResource(Resource):
    def post(self):
        reserva_service = ReservaService(db.session)
        try:
            data = request.get_json()
            reserva = reserva_service.criar_reserva(data)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat()
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class ReservaListResource(Resource):
        
    def get(self, reserva_id):
        reserva_service = ReservaService(db.session)
        try:
            reserva = reserva_service.listar_reserva(reserva_id)
            if not reserva:
                return {"error": "Reserva nao encontrada"}, 404
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat(),
                "hospedes": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in reserva.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, reserva_id):
        reserva_service = ReservaService(db.session)
        try:
            reserva_service.deletar_reserva(reserva_id)
            
            return '', 204
            
        except Exception as e:
            return {"error": str(e)}, 400
        
    def patch(self, reserva_id):
        reserva_service = ReservaService(db.session)
        try:
            data = request.get_json()
            reserva = reserva_service.atualizar_reserva_parcial(reserva_id, data)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat(),
                "hospedes": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in reserva.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
    

    def put(self, reserva_id):
        reserva_service = ReservaService(db.session)
        try:
            data = request.get_json()
            reserva = reserva_service.atualizar_reserva_total(reserva_id, data)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat(),
                "hospedes": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in reserva.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
class ReservaStatusResource(Resource):

    def patch(self, reserva_id):
        reserva_service = ReservaService(db.session)
        try:
            reserva = reserva_service.forcar_status_reserva(reserva_id)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat(),
                "hospedes": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in reserva.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400

class ReservaHospedeResource(Resource):

    def post(self, reserva_id, hospede_id):
        reserva_service = ReservaService(db.session)
        try:
            reserva = reserva_service.adicionar_hospede_a_reserva(reserva_id, hospede_id)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat(),
                "hospedes": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in reserva.hospedes
                ]
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, reserva_id, hospede_id):
        reserva_service = ReservaService(db.session)
        try:
            data = reserva_service.remover_hospede_da_reserva(reserva_id, hospede_id)
            if data is True:
                return { "message": "Hospede removido da reserva com sucesso"}, 200
        except Exception as e:
            return {"error": str(e)}, 400