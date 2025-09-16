from src.controllers.HelloWorld import Hello
from src.controllers.Verificacao import VerificacaoController
from src.controllers.ReservaController import ReservaListResource
from src.controllers.HospedeController import HospedeListResource

def initialize_endpoints(api):
    api.add_resource(Hello, "/hello")

    api.add_resource(VerificacaoController, "/verify_faces")

    api.add_resource(ReservaListResource, "/reserva")

    api.add_resource(HospedeListResource, "/hospede")