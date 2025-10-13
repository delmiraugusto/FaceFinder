from flask import request
from flask_restful import Resource
import os
from src.service.documentData_service import DocumentDataService
from src.models.Base import db
from src.config.auth import require_api_key
from src.models.DocumentData import DocumentData

DOCUMENTDATA_API_KEY = os.getenv("DOCUMENTDATA_API_KEY")

class DocumentDataBaseResource(Resource):
    method_decorators = [require_api_key(DOCUMENTDATA_API_KEY)]

class DocumentDataResource(DocumentDataBaseResource):
    def post(self, hospede_id):
        documentData_service = DocumentDataService(db.session)
        try:
            data = request.get_json()
            documentData = documentData_service.criar_documentData(data, hospede_id)
            return {
                "codigo_uuid": documentData.codigo_uuid,
                "status": str(documentData.status),
                "create_at": documentData.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in documentData.hospedes
                ]
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400
        
class DocumentDataListResource(DocumentDataBaseResource):
        
    def get(self, documentData_id):
        documentData_service = DocumentDataService(db.session)
        try:
            documentData = documentData_service.listar_documentData(documentData_id)
            return {
                "codigo_uuid": documentData.codigo_uuid,
                "status": str(documentData.status),
                "create_at": documentData.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in documentData.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    def delete(self, documentData_id):
        documentData_service = DocumentDataService(db.session)
        try:
            documentData_service.deletar_documentData(documentData_id)
            
            return '', 204
            
        except Exception as e:
            return {"error": str(e)}, 400
    
    def patch(self, documentData_id):
        documentData_service = DocumentDataService(db.session)
        try:
            data = request.get_json()
            documentData = documentData_service.atualizar_documentData_parcial(documentData_id, data)
            return {
                "codigo_uuid": documentData.codigo_uuid,
                "status": str(documentData.status),
                "create_at": documentData.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in documentData.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
    
    def put(self, documentData_id):
        documentData_service = DocumentDataService(db.session)
        try:
            data = request.get_json()
            documentData = documentData_service.atualizar_documentData_total(documentData_id, data)
            return {
                "codigo_uuid": documentData.codigo_uuid,
                "status": str(documentData.status),
                "create_at": documentData.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in documentData.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
class DocumentDataStatusResource(DocumentDataBaseResource):

    def patch(self, documentData_id):
        documentData_service = DocumentDataService(db.session)
        data = request.get_json()
        try:
            documentData = documentData_service.forcar_status_documentData(documentData_id, data['status'])
            return {
                "codigo_uuid": documentData.codigo_uuid,
                "status": str(documentData.status),
                "create_at": documentData.create_at.isoformat(),
                "hospede": [
                    {
                        "codigo_uuid": hospede.codigo_uuid,
                        "status": bool(hospede.status)
                    }
                    for hospede in documentData.hospedes
                ]
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400