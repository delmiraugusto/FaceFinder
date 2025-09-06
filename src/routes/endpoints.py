from src.controllers.HelloWorld import Hello
from src.controllers.Verificacao import VerificacaoController

def initialize_endpoints(api):
    api.add_resource(Hello, "/hello")

    api.add_resource(VerificacaoController, "/verify_faces")