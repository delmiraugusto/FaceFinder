from flask import request
from flask_restful import Resource
from src.service.verificacao_service import verify_faces

class VerificacaoController(Resource):
    def post(self):
        try:
            data = request.get_json()

            if 'document' not in data or 'selfie' not in data:
                return {"error": "Campos 'document' e 'selfie' são obrigatórios."}, 400

            result = verify_faces(data['document'], data['selfie'])
            return result, 200

        except ValueError as ve:
            return {"error": str(ve)}, 400