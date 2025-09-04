from src.controllers.HelloWorld import Hello

def initialize_endpoints(api):
    api.add_resource(Hello, "/hello")