from flask_restful import Resource

class base_prueba(Resource):
    def get(self):
        saludo = "Hola Mundo0"
        return saludo

