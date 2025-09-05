from src.controllers.HelloWorld import Hello
from src.controllers.Verificacao import Verificacao

def initialize_endpoints(api):
    api.add_resource(Hello, "/hello")

    api.add_resource(Verificacao, "/verify_faces")