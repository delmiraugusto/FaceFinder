from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from src.routes.endpoints import initialize_endpoints
from src.models.Base import db
import os

def create_app() -> Flask:

    app = Flask(__name__)
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    # Comando para ativar a venv
    # .\venv\Scripts\Activate.ps1

    # Comando para rodar o programa
    # flask --app manage run --host=0.0.0.0 --port=5001
    
    api = Api(app, prefix="/faceFinder")
    initialize_endpoints(api)

    return app
