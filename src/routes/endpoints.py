from src.controllers.HelloWorld import Hello
from src.controllers.Verificacao import VerificacaoController
from src.controllers.ReservaController import (ReservaHospedeResource, ReservaListResource,
    ReservaResource, ReservaStatusResource)
from src.controllers.HospedeController import HospedeListResource

def initialize_endpoints(api):
    api.add_resource(Hello, "/hello")

    api.add_resource(VerificacaoController, "/verify_faces")

    #Reserva Endpoints
    api.add_resource(ReservaResource, "/reserva")

    api.add_resource(ReservaHospedeResource, "/reserva/<string:reserva_id>/hospede/<string:hospede_id>")

    api.add_resource(ReservaListResource, "/reserva/<string:reserva_id>")

    api.add_resource(ReservaStatusResource, "/reserva/status/<string:reserva_id>")



    api.add_resource(HospedeListResource, "/hospede")
