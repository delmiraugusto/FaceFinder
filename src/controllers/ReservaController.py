from flask import request
from flask_restful import Resource
from src.service.reserva_service import ReservaService
from sqlalchemy.orm import Session
from src.models.Base import db

class ReservaListResource(Resource):

    def post(self):
        data = request.get_json()
        reserva_service = ReservaService(db.session)
        try:
            reserva = reserva_service.criar_reserva(data)
            return {
                "codigo_uuid": reserva.codigo_uuid,
                "numero_reserva": reserva.numero_reserva,
                "status": str(reserva.status),
                "data_checkin": reserva.data_checkin.isoformat()
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
    